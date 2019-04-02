from django.contrib import admin
from .models import CaseScreening, EventScreening, ScreenedUser

@admin.register(CaseScreening)
class CaseScreeningAdmin(admin.ModelAdmin):
    list_display = ['user', 'case_name', 'purpose', 'date', 'counselor', 'registration_lockout_end_time']
    search_fields = ['user__username', 'case_name', 'counselor']
    list_filter = ['purpose', 'date', 'registration_lockout_end_time']

class ScreenedUserInline(admin.TabularInline):
    model = ScreenedUser
    extra = 1

@admin.register(EventScreening)
class EventScreeningAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'start_date', 'end_date', 'counselor', 'approval_status', 'registration_lockout_end_time']
    search_fields = ['event_name', 'counselor']
    list_filter = ['start_date', 'end_date', 'approval_status', 'registration_lockout_end_time']
    inlines = [ScreenedUserInline]
