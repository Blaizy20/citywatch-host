from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('<int:notif_id>/read/', views.mark_read, name='mark_read'),
    path('<int:notif_id>/toggle-read/', views.toggle_read, name='toggle_read'),
    path('<int:notif_id>/delete/', views.delete_notification, name='delete_notification'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
]