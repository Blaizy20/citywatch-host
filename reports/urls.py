from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('announcements/', views.announcement_list, name='announcements'),
    path('announcements/<int:announcement_id>/', views.announcement_detail, name='announcement_detail'),
    path('dashboard/', views.resident_dashboard, name='resident_dashboard'),
    path('', views.report_list, name='report_list'),
    path('new/', views.report_create, name='report_create'),
    path('board/', views.public_board, name='public_board'),
    path('<int:report_id>/', views.report_detail, name='report_detail'),
    path('<int:report_id>/edit/', views.report_edit, name='report_edit'),
    path('<int:report_id>/delete/', views.report_delete, name='report_delete'),
    path('admin/list/', views.admin_report_list, name='admin_report_list'),
    path('admin/announcements/', views.admin_announcement_list, name='admin_announcement_list'),
    path('admin/announcements/<int:announcement_id>/edit/', views.admin_announcement_edit, name='admin_announcement_edit'),
    path('admin/announcements/<int:announcement_id>/delete/', views.admin_announcement_delete, name='admin_announcement_delete'),
    path('admin/<int:report_id>/', views.admin_report_detail, name='admin_report_detail'),
]