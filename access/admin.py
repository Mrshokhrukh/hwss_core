# your_app_name/admin.py
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import PreRecordedUser, Agency, UserAgency, CustomUser
from .resources import PreRecordedUserResource
from django.contrib import messages
from django.urls import path
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
import csv
import io

@admin.register(PreRecordedUser)
class PreRecordedUserAdmin(ImportExportModelAdmin):
    resource_class = PreRecordedUserResource
    list_display = (
        'username', 'email', 'identity_number', 'first_name', 'last_name',
        'is_registered', 'role', 'date_joined', 'is_active'
    )
    list_filter = ('is_registered', 'role', 'is_active', 'is_gyalsung')
    search_fields = (
        'username', 'email', 'identity_number', 'first_name', 'last_name'
    )
    list_per_page = 25
    ordering = ('-date_joined',)
    fieldsets = (
        ('Personal Information', {
            'fields': (
                'username', 'email', 'identity_number', 'nationality',
                'first_name', 'middle_name', 'last_name', 'date_of_birth',
                'gender', 'mob_number', 'profile_picture'
            )
        }),
        ('Address Information', {
            'fields': (
                'perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag'
            )
        }),
        ('Family Information', {
            'fields': (
                'father_name', 'mother_name', 'parent_occupation',
                'guardian_name', 'guardian_occupation', 'parent_status',
                'current_living_with'
            )
        }),
        ('Agency Information', {
            'fields': (
                'agency_name', 'agency_code', 'user_code', 'user_role_agency',
                'user_class', 'user_sub_class'
            )
        }),
        ('Account Information', {
            'fields': (
                'role', 'access_level', 'is_gyalsung', 'academy_code',
                'is_active', 'is_staff', 'is_registered', 'date_joined'
            )
        }),
    )
    readonly_fields = ('date_joined',)
    actions = ['mark_as_registered', 'export_as_csv_template']

    def mark_as_registered(self, request, queryset):
        updated = queryset.update(is_registered=True)
        self.message_user(
            request,
            f"{updated} user(s) marked as registered.",
            messages.SUCCESS
        )
    mark_as_registered.short_description = "Mark selected users as registered"

    def export_as_csv_template(self, request, queryset):
        # Generate a CSV template with only required fields
        required_fields = [
            'username', 'identity_number', 'nationality', 'first_name',
            'last_name', 'date_of_birth', 'gender', 'email', 'mob_number',
            'perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag'
        ]
        optional_fields = [
            'middle_name', 'father_name', 'mother_name', 'profile_picture',
            'is_gyalsung', 'academy_code', 'role', 'access_level',
            'agency_name', 'agency_code', 'user_code', 'parent_occupation',
            'guardian_name', 'guardian_occupation', 'parent_status',
            'current_living_with', 'user_role_agency', 'user_class',
            'user_sub_class'
        ]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="pre_recorded_user_template.csv"'
        writer = csv.writer(response)
        writer.writerow(required_fields + optional_fields)
        return response
    export_as_csv_template.short_description = "Download CSV template for bulk upload"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'download-csv-template/',
                self.admin_site.admin_view(self.download_csv_template),
                name='pre_recorded_user_download_csv_template'
            ),
        ]
        return custom_urls + urls

    def download_csv_template(self, request):
        # Redirect to the action to download the CSV template
        return self.export_as_csv_template(request, self.model.objects.none())

    def get_actions(self, request):
        actions = super().get_actions(request)
        # Add actions to the admin interface
        return actions

    def save_model(self, request, obj, form, change):
        # Custom save logic if needed
        super().save_model(request, obj, form, change)

# Register other models if not already registered
@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('agency_name', 'agency_code', 'present_dzongkhag')
    search_fields = ('agency_name', 'agency_code')
    list_filter = ('present_dzongkhag',)

@admin.register(UserAgency)
class UserAgencyAdmin(admin.ModelAdmin):
    list_display = ('user', 'agency', 'user_role_agency')
    search_fields = ('user__username', 'agency__agency_name')
    list_filter = ('user_role_agency',)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('role', 'is_active', 'is_staff')
    fieldsets = (
        ('Personal Information', {
            'fields': (
                'username', 'email', 'first_name', 'middle_name', 'last_name',
                'identity_number', 'nationality', 'date_of_birth', 'gender',
                'mob_number', 'profile_picture'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups',
                'user_permissions'
            )
        }),
        ('Agency and Address', {
            'fields': (
                'active_agency', 'perm_add_village', 'perm_add_gewog',
                'perm_add_dzongkhag', 'ps_add_village', 'ps_add_gewog',
                'ps_add_dzongkhag'
            )
        }),
        ('Account Details', {
            'fields': (
                'role', 'access_level', 'is_gyalsung', 'academy_code',
                'registration_method', 'date_joined'
            )
        }),
    )
    readonly_fields = ('date_joined',)