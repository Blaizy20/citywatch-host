from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from .models import Announcement, Report, ReportStatusLog, ReportFeedback
from .forms import ReportForm, ReportFeedbackForm
from notifications.utils import create_notification


def admin_check(user):
    return user.is_staff or user.is_superuser


def home(request):
    return render(request, 'reports/home.html', {
        'announcements': Announcement.objects.filter(is_published=True)[:3],
        'resolved_count': Report.objects.filter(status='resolved').count(),
        'participant_count': User.objects.count(),
    })


@login_required
def announcement_list(request):
    announcements = Announcement.objects.filter(is_published=True)
    announcement_type = request.GET.get('type', '').strip()
    search_query = request.GET.get('q', '').strip()
    if announcement_type in {'news', 'advisory'}:
        announcements = announcements.filter(announcement_type=announcement_type)
    if search_query:
        announcements = announcements.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )
    return render(request, 'reports/announcements.html', {
        'announcements': announcements,
        'announcement_type': announcement_type,
        'search_query': search_query,
    })


@login_required
def resident_dashboard(request):
    reports = Report.objects.filter(resident=request.user)
    search_query = request.GET.get('q', '').strip()
    if search_query:
        reports = reports.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(barangay__icontains=search_query)
        )
    active_reports = reports.exclude(status__in=['resolved', 'closed']).order_by('-date_submitted')[:5]

    stats = {
        'total': reports.count(),
        'pending': reports.filter(status='pending').count(),
        'in_progress': reports.filter(status='in_progress').count(),
        'resolved': reports.filter(status='resolved').count(),
    }
    
    # Context for other SPA tabs
    status_filter = request.GET.get('status', '').strip()
    category_filter = request.GET.get('category', '').strip()

    if status_filter:
        reports = reports.filter(status=status_filter)

    public_reports = Report.objects.all()
    if status_filter:
        public_reports = public_reports.filter(status=status_filter)
    if category_filter:
        public_reports = public_reports.filter(category=category_filter)
    if search_query:
        public_reports = public_reports.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(barangay__icontains=search_query)
        )
    public_reports = public_reports.order_by('-date_submitted')[:20]
    
    announcement_type = request.GET.get('type', '').strip()
    all_announcements = Announcement.objects.filter(is_published=True).order_by('-date_published')
    if announcement_type:
        all_announcements = all_announcements.filter(announcement_type=announcement_type)
    
    from notifications.models import Notification
    all_notifications = Notification.objects.filter(user=request.user).order_by('-date_created')
    
    from accounts.models import Profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    return render(request, 'reports/dashboard.html', {
        'reports': reports, # All my reports for the My Reports tab
        'active_reports': active_reports, # Just the 5 active ones for the Overview tab
        'stats': stats,
        'announcements': all_announcements[:4] if not announcement_type else all_announcements[:4], # Overview announcements
        'all_announcements': all_announcements, # Announcements tab
        'public_reports': public_reports, # Public board tab
        'public_total': Report.objects.count(),
        'public_resolved': Report.objects.filter(status='resolved').count(),
        'all_notifications': all_notifications, # Notifications tab
        'form': ReportForm(), # New Report tab
        'search_query': search_query,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'announcement_type': announcement_type,
        'profile': profile,
    })


@login_required
def report_list(request):
    reports = Report.objects.filter(resident=request.user)
    status_filter = request.GET.get('status')
    if status_filter:
        reports = reports.filter(status=status_filter)

    stats = {
        'total': reports.count(),
        'pending': reports.filter(status='pending').count(),
        'in_progress': reports.filter(status='in_progress').count(),
        'resolved': reports.filter(status='resolved').count(),
    }

    return render(request, 'reports/report_list.html', {'reports': reports, 'stats': stats, 'status_filter': status_filter})


@login_required
def report_create(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.resident = request.user
            report.save()

            ReportStatusLog.objects.create(
                report=report,
                old_status='',
                new_status='pending',
                changed_by=request.user,
                notes='Report submitted'
            )

            create_notification(
                user=request.user,
                message=f'Your report <b>{report.title}</b> has been submitted.',
                report=report,
                notif_type='status_update'
            )
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'report_id': report.id})

            messages.success(request, 'Report submitted successfully!')
            return redirect('report_detail', report_id=report.id)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
            messages.error(request, 'Please check the form for errors.')
    else:
        form = ReportForm()

    return render(request, 'reports/report_form.html', {'form': form})


@login_required
def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    status_logs = report.status_logs.all()
    feedback = getattr(report, 'feedback', None)
    feedback_form = None

    if report.status == 'resolved' and not feedback:
        feedback_form = ReportFeedbackForm()

    if request.method == 'POST' and report.status == 'resolved' and not feedback:
        feedback_form = ReportFeedbackForm(request.POST)
        if feedback_form.is_valid():
            fb = feedback_form.save(commit=False)
            fb.report = report
            fb.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('report_detail', report_id=report.id)

    return render(request, 'reports/report_detail.html', {
        'report': report,
        'status_logs': status_logs,
        'feedback': feedback,
        'feedback_form': feedback_form,
    })


@login_required
def report_edit(request, report_id):
    report = get_object_or_404(Report, id=report_id, resident=request.user)

    if report.status != 'pending':
        messages.error(request, 'You can only edit reports that are still pending.')
        return redirect('report_detail', report_id=report.id)

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'report_id': report.id})
            messages.success(request, 'Report updated successfully!')
            return redirect('report_detail', report_id=report.id)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = ReportForm(instance=report)

    return render(request, 'reports/report_form.html', {'form': form, 'editing': True})


@login_required
def report_delete(request, report_id):
    report = get_object_or_404(Report, id=report_id, resident=request.user)

    if report.status != 'pending':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'You can only delete pending reports.'}, status=400)
        messages.error(request, 'You can only delete reports that are still pending.')
        return redirect('report_detail', report_id=report.id)

    if request.method == 'POST':
        report.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        messages.success(request, 'Report deleted.')
        return redirect('report_list')

    return render(request, 'reports/report_confirm_delete.html', {'report': report})


def public_board(request):
    reports = Report.objects.all().order_by('-date_submitted')
    status_filter = request.GET.get('status')
    category_filter = request.GET.get('category')
    search_query = request.GET.get('q', '').strip()
    if status_filter:
        reports = reports.filter(status=status_filter)
    if category_filter:
        reports = reports.filter(category=category_filter)
    if search_query:
        reports = reports.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(barangay__icontains=search_query)
        )

    return render(request, 'reports/public_board.html', {
        'reports': reports[:20],
        'total_reports': Report.objects.count(),
        'resolved_count': Report.objects.filter(status='resolved').count(),
        'average_resolution_days': 0,
        'search_query': search_query,
        'status_filter': status_filter,
        'category_filter': category_filter,
    })


@login_required
@user_passes_test(admin_check)
def admin_report_list(request):
    reports = Report.objects.all().order_by('-date_submitted')

    status_filter = request.GET.get('status', '').strip()
    category_filter = request.GET.get('category', '').strip()
    search_query = request.GET.get('q', '').strip()
    view_mode = request.GET.get('view', 'list')
    if view_mode not in {'list', 'visual'}:
        view_mode = 'list'

    if status_filter:
        reports = reports.filter(status=status_filter)
    if category_filter:
        reports = reports.filter(category=category_filter)
    if search_query:
        reports = reports.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(barangay__icontains=search_query) |
            Q(resident__username__icontains=search_query)
        )

    return render(request, 'reports/admin_report_list.html', {
        'reports': reports,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'search_query': search_query,
        'view_mode': view_mode,
        'category_choices': Report.CATEGORY_CHOICES,
    })


@login_required
@user_passes_test(admin_check)
def admin_report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    status_logs = report.status_logs.all()
    assignment = getattr(report, 'assignment', None)

    from assignments.models import Department
    departments = list(Department.objects.all())
    preferred_departments = ['Fire', 'Health', 'DPWH', 'Barangay Tanod']
    departments.sort(key=lambda department: (
        preferred_departments.index(department.name)
        if department.name in preferred_departments else len(preferred_departments),
        department.name.lower(),
    ))

    return render(request, 'reports/admin_report_detail.html', {
        'report': report,
        'status_logs': status_logs,
        'assignment': assignment,
        'departments': departments,
    })