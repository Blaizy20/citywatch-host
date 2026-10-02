import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone

from .models import OTPChallenge, Profile


OTP_LIFETIME = timedelta(minutes=10)
OTP_RESEND_WAIT = timedelta(seconds=60)
OTP_MAX_ATTEMPTS = 5


def _issue_otp(email, purpose, payload=None):
    latest = OTPChallenge.objects.filter(email__iexact=email, purpose=purpose).order_by('-created_at').first()
    if latest and timezone.now() - latest.created_at < OTP_RESEND_WAIT:
        raise ValueError('Please wait a minute before requesting another code.')

    action = 'signup' if purpose == 'registration' else 'password reset'
    code = f'{secrets.randbelow(1_000_000):06d}'
    subject = 'Your CityWatch verification code'
    body = (
        f'Your CityWatch verification code is {code}.\n\n'
        f'Use this code to complete your {action}.\n'
        'This code expires in 10 minutes.\n\n'
        'If you did not request this code, you can ignore this email.'
    )
    
    # DEV HELPER: Print the code to the terminal so it's easy to find!
    print(f"\n{'='*40}\n[DEV] VERIFICATION CODE FOR {email}: {code}\n{'='*40}\n")
    
    html_message = render_to_string('accounts/email_verification.html', {
        'action': action,
        'code': code,
    })
    
    challenge = OTPChallenge.objects.create(
        email=email,
        purpose=purpose,
        code_hash=make_password(code),
        payload=payload or {},
        expires_at=timezone.now() + OTP_LIFETIME,
    )
    OTPChallenge.objects.filter(email__iexact=email, purpose=purpose).exclude(pk=challenge.pk).delete()

    try:
        sent = send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,
        )
        if not sent:
            raise RuntimeError('Email backend did not send the message.')
    except Exception:
        challenge.delete()
        raise
    return challenge


def _valid_otp(challenge, submitted_code):
    if challenge.expires_at <= timezone.now() or challenge.attempts >= OTP_MAX_ATTEMPTS:
        return False
    if not check_password(submitted_code, challenge.code_hash):
        challenge.attempts += 1
        challenge.save(update_fields=['attempts'])
        return False
    return True


def admin_check(user):
    return user.is_staff or user.is_superuser


def landing_view(request):
    from reports.models import Report

    # Removed redirect so authenticated users can see the landing page

    recent_reports = Report.objects.all().order_by('-date_submitted')[:6]
    total_reports = Report.objects.count()
    resolved_count = Report.objects.filter(status='resolved').count()

    return render(request, 'accounts/landing.html', {
        'recent_reports': recent_reports,
        'total_reports': total_reports,
        'resolved_count': resolved_count,
    })


def register_view(request):
    from reports.models import Report
    from django.http import JsonResponse
    from django.urls import reverse

    recent_reports = Report.objects.all().order_by('-date_submitted')[:4]

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        phone = request.POST.get('mobile', '').strip()
        barangay = request.POST.get('barangay', '').strip()
        age = request.POST.get('age') or None
        sex = request.POST.get('sex', '').strip()
        address = request.POST.get('address', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        def registration_error(message):
            if is_ajax:
                return JsonResponse({'success': False, 'error': message})
            messages.error(request, message)
            return render(request, 'accounts/register.html', {'recent_reports': recent_reports})

        if password != confirm_password:
            return registration_error('Passwords do not match.')

        try:
            validate_password(password)
        except ValidationError:
            return registration_error('Please choose a stronger password.')

        if User.objects.filter(username=username).exists():
            return registration_error('Username already taken.')

        if not email or User.objects.filter(email__iexact=email).exists():
            return registration_error('This email address is already in use.')

        try:
            challenge = _issue_otp(email, 'registration', {
                'username': username,
                'password_hash': make_password(password),
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone,
                'barangay': barangay,
                'age': age,
                'sex': sex,
                'address': address,
            })
        except ValueError as error:
            return registration_error(str(error))
        except Exception:
            return registration_error('We could not send your code. Check your email settings and try again.')

        request.session['registration_otp_id'] = challenge.pk

        if is_ajax:
            return JsonResponse({'success': True, 'redirect': reverse('verify_email')})

        return redirect('verify_email')

    return render(request, 'accounts/register.html', {'recent_reports': recent_reports})


def verify_email_view(request):
    challenge_id = request.session.get('registration_otp_id')
    challenge = OTPChallenge.objects.filter(pk=challenge_id, purpose='registration').first()
    if not challenge:
        messages.error(request, 'Start registration again to request a new verification code.')
        return redirect('register')

    error = ''
    notice = ''
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if request.method == 'POST' and request.POST.get('action') == 'resend':
        try:
            challenge = _issue_otp(challenge.email, 'registration', challenge.payload)
            request.session['registration_otp_id'] = challenge.pk
            notice = 'A new verification code has been sent.'
        except ValueError as exception:
            error = str(exception)
        except Exception:
            error = 'We could not send your code. Check your email settings and try again.'
            
        if is_ajax:
            from django.http import JsonResponse
            if error:
                return JsonResponse({'success': False, 'error': error})
            return JsonResponse({'success': True, 'notice': notice})
    elif request.method == 'POST':
        code = request.POST.get('code', '').strip()
        if not code.isdigit() or len(code) != 6 or not _valid_otp(challenge, code):
            error = 'That code is incorrect, expired, or has reached its attempt limit.'
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                from django.http import JsonResponse
                return JsonResponse({'success': False, 'error': error})
        else:
            data = challenge.payload
            if User.objects.filter(username=data['username']).exists() or User.objects.filter(email__iexact=challenge.email).exists():
                challenge.delete()
                request.session.pop('registration_otp_id', None)
                messages.error(request, 'That username or email is already registered. Please register again.')
                return redirect('register')

            with transaction.atomic():
                user = User(
                    username=data['username'],
                    email=challenge.email,
                    password=data['password_hash'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    is_active=True,
                )
                user.save()
                Profile.objects.create(
                    user=user,
                    role='resident',
                    phone_number=data['phone'],
                    barangay=data['barangay'],
                    age=data['age'],
                    sex=data['sex'],
                    address=data['address'],
                )
                challenge.delete()
            request.session.pop('registration_otp_id', None)
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                from django.urls import reverse
                from django.http import JsonResponse
                return JsonResponse({'success': True, 'redirect': reverse('login')})
                
            messages.success(request, 'Email verified. Your account is ready; you can now log in.')
            return redirect('login')

    return render(request, 'accounts/verify_email.html', {
        'email': challenge.email,
        'error': error,
        'notice': notice,
        'can_resend': timezone.now() - challenge.created_at >= OTP_RESEND_WAIT,
    })


def password_reset_view(request):
    if request.method == 'GET':
        for key in ('password_reset_started', 'password_reset_email', 'password_reset_otp_id'):
            request.session.pop(key, None)

    error = ''
    notice = ''
    reset_started = request.session.get('password_reset_started', False)
    email = request.session.get('password_reset_email', '')
    challenge = OTPChallenge.objects.filter(
        pk=request.session.get('password_reset_otp_id'),
        purpose='password_reset',
    ).first()

    if request.method == 'POST' and request.POST.get('action') == 'request_code':
        email = request.POST.get('email', '').strip().lower()
        request.session['password_reset_started'] = True
        request.session['password_reset_email'] = email
        if challenge and challenge.email.lower() != email:
            request.session.pop('password_reset_otp_id', None)
            challenge = None
        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if user:
            try:
                challenge = _issue_otp(email, 'password_reset')
                request.session['password_reset_otp_id'] = challenge.pk
            except ValueError as exception:
                error = str(exception)
            except Exception:
                error = 'We could not send your code. Check your email settings and try again.'
        if not error:
            notice = 'If an active account uses that email, a verification code has been sent.'
        reset_started = True
    elif request.method == 'POST' and request.POST.get('action') == 'resend_code':
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        email = request.session.get('password_reset_email', '')
        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if user:
            try:
                challenge = _issue_otp(email, 'password_reset')
                request.session['password_reset_otp_id'] = challenge.pk
            except ValueError as exception:
                error = str(exception)
            except Exception:
                error = 'We could not send your code. Check your email settings and try again.'
        if not error:
            notice = 'If an active account uses that email, a verification code has been sent.'
        if is_ajax:
            from django.http import JsonResponse
            if error:
                return JsonResponse({'success': False, 'error': error})
            return JsonResponse({'success': True, 'notice': notice})
        reset_started = True
    elif request.method == 'POST' and request.POST.get('action') == 'reset_password':
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        invalid_code = False
        if not challenge or challenge.email.lower() != email.lower():
            error = 'Request a new code to continue.'
            invalid_code = True
        elif not _valid_otp(challenge, request.POST.get('code', '').strip()):
            error = 'That code is incorrect, expired, or has reached its attempt limit.'
            invalid_code = True
        else:
            user = User.objects.filter(email__iexact=email, is_active=True).first()
            new_password = request.POST.get('new_password', '')
            confirm_password = request.POST.get('confirm_password', '')
            if not user:
                error = 'That code is invalid or expired. Request a new one to continue.'
            elif new_password != confirm_password:
                error = 'The passwords do not match.'
            else:
                try:
                    validate_password(new_password, user=user)
                except ValidationError:
                    error = 'Please choose a stronger password.'
                else:
                    user.set_password(new_password)
                    user.save(update_fields=['password'])
                    OTPChallenge.objects.filter(email__iexact=email, purpose='password_reset').delete()
                    for key in ('password_reset_started', 'password_reset_email', 'password_reset_otp_id'):
                        request.session.pop(key, None)
                    if is_ajax:
                        from django.urls import reverse
                        from django.http import JsonResponse
                        return JsonResponse({'success': True, 'redirect': reverse('login')})
                    messages.success(request, 'Password updated. Log in with your new password.')
                    return redirect('login')
        
        if is_ajax and error:
            from django.http import JsonResponse
            return JsonResponse({'success': False, 'error': error, 'invalid_code': invalid_code})
            
        reset_started = True

    return render(request, 'accounts/password_reset.html', {
        'email': email,
        'reset_started': reset_started,
        'error': error,
        'notice': notice,
        'can_resend': not challenge or timezone.now() - challenge.created_at >= OTP_RESEND_WAIT,
        'has_challenge': challenge is not None,
    })


def login_view(request):
    from reports.models import Report
    from django.urls import reverse
    from django.http import JsonResponse

    recent_reports = Report.objects.all().order_by('-date_submitted')[:4]

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            url = reverse('analytics_dashboard') if (user.is_staff or user.is_superuser) else reverse('resident_dashboard')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect': url})
            return redirect(url)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False})
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html', {'recent_reports': recent_reports})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.phone_number = request.POST.get('phone_number')
        profile.barangay = request.POST.get('barangay')
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            from django.http import JsonResponse
            return JsonResponse({
                'success': True,
                'message': 'Profile updated successfully.',
                'phone_number': profile.phone_number,
                'barangay': profile.barangay,
                'profile_picture_url': profile.profile_picture.url if profile.profile_picture else None
            })
            
        messages.success(request, 'Profile updated successfully')
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
@user_passes_test(admin_check)
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
@user_passes_test(admin_check)
def toggle_staff(request, user_id):
    target_user = User.objects.get(id=user_id)
    if request.method == 'POST' and target_user != request.user:
        target_user.is_staff = not target_user.is_staff
        target_user.save()
        messages.success(request, f'Updated staff status for {target_user.username}.')
    return redirect('user_list')