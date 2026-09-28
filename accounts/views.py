from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Profile


def admin_check(user):
    return user.is_staff or user.is_superuser


def landing_view(request):
    from reports.models import Report

    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('analytics_dashboard')
        else:
            return redirect('resident_dashboard')

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
    recent_reports = Report.objects.all().order_by('-date_submitted')[:4]

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('mobile')
        barangay = request.POST.get('barangay')
        age = request.POST.get('age') or None
        sex = request.POST.get('sex', '').strip()
        address = request.POST.get('address', '').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if password != confirm_password:
            if is_ajax:
                return JsonResponse({'success': False, 'error': 'Passwords do not match.'})
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/register.html', {'recent_reports': recent_reports})

        try:
            validate_password(password)
        except ValidationError as error:
            if is_ajax:
                return JsonResponse({'success': False, 'error': ' '.join(error.messages)})
            messages.error(request, ' '.join(error.messages))
            return render(request, 'accounts/register.html', {'recent_reports': recent_reports})

        if User.objects.filter(username=username).exists():
            if is_ajax:
                return JsonResponse({'success': False, 'error': 'Username already taken.'})
            messages.error(request, 'Username already taken')
            return render(request, 'accounts/register.html', {'recent_reports': recent_reports})

        if User.objects.filter(email=email).exists():
            if is_ajax:
                return JsonResponse({'success': False, 'error': 'Email already registered.'})
            messages.error(request, 'Email already registered')
            return render(request, 'accounts/register.html', {'recent_reports': recent_reports})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        Profile.objects.create(
            user=user,
            role='resident',
            phone_number=phone,
            barangay=barangay,
            age=age,
            sex=sex,
            address=address,
        )

        if is_ajax:
            from django.urls import reverse
            return JsonResponse({'success': True, 'redirect': reverse('login')})

        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')

    return render(request, 'accounts/register.html', {'recent_reports': recent_reports})


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