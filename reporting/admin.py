from django.contrib import admin
from .models import Reporting

class ReportingAdmin(admin.ModelAdmin):
    list_display = ['user', 'agency_code', 'agency_name', 'present_dzongkhag', 'present_gewog', 'present_village', 'user_code']

# Register the Reporting model with the custom admin class
admin.site.register(Reporting, ReportingAdmin)
