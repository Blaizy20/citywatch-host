from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import landing_view
from django.core.management import call_command
from django.http import HttpResponse

def run_migration_view(request):
    try:
        call_command('migrate')
        call_command('loaddata', 'datadump.json')
        return HttpResponse("Migration and data load successful! You can now go to the homepage.")
    except Exception as e:
        return HttpResponse(f"Error: {e}")

urlpatterns = [
    path('run-migration-now/', run_migration_view),
    path('', landing_view, name='landing'),
    path('admin/', admin.site.urls),
    path('reports/', include('reports.urls')),
    path('accounts/', include('accounts.urls')),
    path('assign/', include('assignments.urls')),
    path('notifications/', include('notifications.urls')),
    path('analytics/', include('analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)