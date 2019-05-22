from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/access/', include('access.urls')),
    path('api/v1/settings/', include('settings_module.urls')),
    path('api/v1/measurement/', include('measurement.urls')),
    path('api/v1/monitoring/', include('monitoring.urls')),
    path('api/v1/reporting/', include('reporting.urls')),
    path('api/v1/screening/', include('screening.urls')),
    path('api/v1/gyalsung_users/', include('gyalsung_users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
