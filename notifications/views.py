from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})


@login_required
def mark_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    if notif.report:
        return redirect('report_detail', report_id=notif.report.id)
    return redirect('notification_list')


@login_required
def toggle_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    if request.method == 'POST':
        notif.is_read = not notif.is_read
        notif.save(update_fields=['is_read'])
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            from django.http import JsonResponse
            return JsonResponse({'status': 'success', 'is_read': notif.is_read})
    return redirect('notification_list')


@login_required
def delete_notification(request, notif_id):
    if request.method == 'POST':
        notif = get_object_or_404(Notification, id=notif_id, user=request.user)
        notif.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            from django.http import JsonResponse
            return JsonResponse({'status': 'success'})
    return redirect('notification_list')

@login_required
def mark_all_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('notification_list')