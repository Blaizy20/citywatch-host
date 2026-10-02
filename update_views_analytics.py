import codecs
import re

content = codecs.open('d:/citywatch/analytics/views.py', 'r', 'utf-8').read()

new_view = '''@login_required
@user_passes_test(admin_check)
def reports_analytics(request):
    from django.utils import timezone
    from datetime import timedelta, datetime
    from django.db.models.functions import TruncDate

    timeframe = request.GET.get('timeframe', 'all')
    custom_start = request.GET.get('custom_start')
    custom_end = request.GET.get('custom_end')
    
    base_qs = Report.objects.all()
    
    now = timezone.now()
    if timeframe == '7':
        base_qs = base_qs.filter(date_submitted__gte=now - timedelta(days=7))
    elif timeframe == '30':
        base_qs = base_qs.filter(date_submitted__gte=now - timedelta(days=30))
    elif timeframe == '90':
        base_qs = base_qs.filter(date_submitted__gte=now - timedelta(days=90))
    elif timeframe == 'custom':
        if custom_start:
            try:
                start_dt = datetime.strptime(custom_start, '%Y-%m-%d').replace(tzinfo=timezone.utc)
                base_qs = base_qs.filter(date_submitted__gte=start_dt)
            except ValueError:
                pass
        if custom_end:
            try:
                # Add 1 day to include the entire end date
                end_dt = datetime.strptime(custom_end, '%Y-%m-%d').replace(tzinfo=timezone.utc) + timedelta(days=1)
                base_qs = base_qs.filter(date_submitted__lt=end_dt)
            except ValueError:
                pass

    total_reports = base_qs.count()

    reports_by_category = base_qs.values('category').annotate(count=Count('id')).order_by('-count')
    reports_by_barangay = base_qs.values('barangay').annotate(count=Count('id')).order_by('-count')
    reports_by_status = base_qs.values('status').annotate(count=Count('id')).order_by('-count')

    # Trend Data (Reports over time)
    trend_qs = base_qs.annotate(date=TruncDate('date_submitted')).values('date').annotate(count=Count('id')).order_by('date')
    trend_data = [{'date': item['date'].strftime('%b %d') if item['date'] else 'Unknown', 'count': item['count']} for item in trend_qs]

    category_data = []
    for item in reports_by_category:
        percent = round((item['count'] / total_reports) * 100, 1) if total_reports else 0
        category_data.append({'label': item['category'], 'count': item['count'], 'percent': percent})

    barangay_data = []
    for item in reports_by_barangay:
        percent = round((item['count'] / total_reports) * 100, 1) if total_reports else 0
        barangay_data.append({'label': item['barangay'], 'count': item['count'], 'percent': percent})

    status_data = []
    for item in reports_by_status:
        percent = round((item['count'] / total_reports) * 100, 1) if total_reports else 0
        status_data.append({'label': item['status'], 'count': item['count'], 'percent': percent})

    resolved_reports = base_qs.filter(status='resolved').annotate(
        resolution_time=ExpressionWrapper(
            F('date_updated') - F('date_submitted'),
            output_field=DurationField()
        )
    )

    avg_resolution = None
    avg_res_detailed = None
    if resolved_reports.exists():
        total_seconds = sum([r.resolution_time.total_seconds() for r in resolved_reports])
        avg_seconds = total_seconds / resolved_reports.count()
        avg_resolution = round(avg_seconds / 86400, 1)
        
        # Detailed calculation
        days = int(avg_seconds // 86400)
        hours = int((avg_seconds % 86400) // 3600)
        minutes = int((avg_seconds % 3600) // 60)
        avg_res_detailed = f"{days}d {hours}h {minutes}m" if days > 0 else f"{hours}h {minutes}m"

    context = {
        'total_reports': total_reports,
        'category_data': category_data,
        'barangay_data': barangay_data,
        'status_data': status_data,
        'trend_data': trend_data,
        'avg_resolution_days': avg_resolution,
        'avg_res_detailed': avg_res_detailed,
        'timeframe': timeframe,
        'custom_start': custom_start or '',
        'custom_end': custom_end or ''
    }

    return render(request, 'analytics/reports_analytics.html', context)
'''

pattern = re.compile(r'@login_required\s+@user_passes_test\(admin_check\)\s+def reports_analytics\(request\):.*?(?=\n\n\n|\Z)', re.DOTALL)
new_content = pattern.sub(new_view.strip(), content)

codecs.open('d:/citywatch/analytics/views.py', 'w', 'utf-8').write(new_content)
