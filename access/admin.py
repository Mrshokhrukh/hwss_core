# your_app_name/admin.py
import csv
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin

# Import your models and resources
from .models import Agency, CustomUser, PreRecordedUser, UserAgency
from .resources import PreRecordedUserResource # Make sure this resource.py file exists

# --- Inlines for a More Integrated Experience ---

class UserAgencyInline(admin.StackedInline):
    """
    Manages the User-Agency relationship directly within the CustomUser admin page.
    This is much more user-friendly than managing it through a separate admin page.
    'StackedInline' is used for a better layout given the number of fields.
    """
    model = UserAgency
    can_delete = False
    verbose_name_plural = 'Agency Details'
    fk_name = 'user'
    
    # Organize the inline form into logical, collapsible sections
    fieldsets = (
        ('Agency Association', {
            'fields': ('agency', 'user_code', 'user_role_agency')
        }),
        ('Academic Information', {
            'classes': ('collapse',), # This section will be collapsed by default
            'fields': ('user_class', 'user_stream', 'user_sub_class')
        }),
        ('Family/Guardian Information', {
            'classes': ('collapse',),
            'fields': ('parent_occupation', 'guardian_name', 'guardian_occupation', 'parent_status', 'current_living_with')
        }),
    )
    
    # Use 'raw_id_fields' for better performance if you have many agencies
    raw_id_fields = ('agency',)

# --- ModelAdmin Configurations ---

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin for managing CustomUser.
    Inherits from UserAdmin for secure auth features,
    with merged fieldsets and inline agency support.
    """

    inlines = (UserAgencyInline,)

    list_display = (
        "username",
        "email",
        "get_full_name",
        "role",
        "is_active",
        "is_staff",
        "date_joined",
    )
    list_filter = (
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "gyalsung_status",
        "is_gyalsung",
        "gyalsung_screening_status",
        "groups",
    )
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "identity_number",
    )
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "email",
                    "identity_number",
                    "nationality",
                    "date_of_birth",
                    "gender",
                    "mob_number",
                    "profile_picture",
                )
            },
        ),
        (
            "Gyalsung Information",
            {
                "fields": (
                    "is_gyalsung",
                    "gyalsung_status",
                    "gyalsung_screening_status",
                    "gyalsung_referral_status",
                    "guard_mob_number",
                    "hospital_name",
                    "hospital_dzongkhag",
                    "appointment_date",
                    "academy_name",
                    "academy_code",
                    "personal_number",
                )
            },
        ),
        (
            "Agency and Address",
            {
                "fields": (
                    "active_agency",
                    "perm_add_village",
                    "perm_add_gewog",
                    "perm_add_dzongkhag",
                    "ps_add_village",
                    "ps_add_gewog",
                    "ps_add_dzongkhag",
                )
            },
        ),
        (
            "Permissions & Role",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "role",
                    "access_level",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "registration_method",
                    "is_old_case_user",
                    "date_joined",
                    "last_login",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Custom Fields",
            {"fields": ("first_name", "last_name", "role", "identity_number")},
        ),
    )

    readonly_fields = ("date_joined", "last_login")

    actions = ["activate_users", "deactivate_users"]

    def get_full_name(self, obj):
        return f"{obj.first_name or ''} {obj.last_name or ''}".strip()

    get_full_name.short_description = "Full Name"

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected users have been activated.", messages.SUCCESS)

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected users have been deactivated.", messages.SUCCESS)



@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('agency_name', 'agency_code', 'agency_parent', 'present_dzongkhag')
    search_fields = ('agency_name', 'agency_code', 'agency_parent')
    list_filter = ('present_dzongkhag',)
    ordering = ('agency_name',)


@admin.register(PreRecordedUser)
class PreRecordedUserAdmin(ImportExportModelAdmin):
    """
    Admin for pre-recorded users with import/export functionality and a cleaner layout.
    """
    resource_class = PreRecordedUserResource
    list_display = ('username', 'email', 'identity_number', 'first_name', 'last_name', 'is_registered', 'role')
    list_filter = ('is_registered', 'role', 'is_gyalsung', 'agency_name')
    search_fields = ('username', 'email', 'identity_number', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined',)
    
    fieldsets = (
        ('Primary Details', {'fields': ('username', 'email', 'identity_number', 'is_registered')}),
        ('Personal Info', {'classes': ('collapse',), 'fields': (('first_name', 'middle_name', 'last_name'), ('date_of_birth', 'gender'), 'nationality', 'mob_number', 'profile_picture')}),
        ('Family Info', {'classes': ('collapse',), 'fields': ('father_name', 'mother_name', 'parent_occupation', 'guardian_name', 'guardian_occupation', 'parent_status', 'current_living_with')}),
        ('Address', {'classes': ('collapse',), 'fields': ('perm_add_dzongkhag', 'perm_add_gewog', 'perm_add_village')}),
        ('Agency & Academic', {'classes': ('collapse',), 'fields': ('agency_name', 'agency_code', 'user_code', 'user_role_agency', 'user_class', 'user_sub_class')}),
        ('System & Role', {'classes': ('collapse',), 'fields': ('role', 'access_level', 'is_gyalsung', 'academy_code', 'is_active', 'is_staff', 'date_joined')}),
    )
    
    actions = ['mark_as_registered', 'export_as_csv_template']

    def mark_as_registered(self, request, queryset):
        """Marks selected users as registered."""
        updated = queryset.update(is_registered=True)
        self.message_user(request, f"{updated} user(s) successfully marked as registered.", messages.SUCCESS)
    mark_as_registered.short_description = "Mark selected as registered"

    def export_as_csv_template(self, request, queryset):
        """Generates a CSV file with headers for bulk importing pre-recorded users."""
        field_names = [
            'username', 'identity_number', 'nationality', 'first_name', 'last_name',
            'date_of_birth', 'gender', 'email', 'mob_number', 'perm_add_village',
            'perm_add_gewog', 'perm_add_dzongkhag', 'middle_name', 'father_name', 'mother_name', 
            'is_gyalsung', 'academy_code', 'role', 'access_level', 'agency_name', 'agency_code',
            'user_code', 'parent_occupation', 'guardian_name', 'guardian_occupation',
            'parent_status', 'current_living_with', 'user_role_agency', 'user_class',
            'user_sub_class'
        ]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="pre_recorded_user_template.csv"'
        writer = csv.writer(response)
        writer.writerow(field_names)
        return response
    export_as_csv_template.short_description = "Download CSV template for bulk upload"

@admin.register(UserAgency)
class UserAgencyAdmin(admin.ModelAdmin):
    list_display = ("user", "agency", "user_role_agency")
    search_fields = ("user__username", "agency__agency_name")
    list_filter = ("user_role_agency",)


