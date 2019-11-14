from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser, PreRecordedUser, Agency, UserAgency
from django.contrib.auth.admin import UserAdmin


class UserAgencyInline(admin.TabularInline):
    model = UserAgency
    fk_name = 'user'
    extra = 1
    fields = (
        'agency',
        'user_code',
        'user_role_agency',
        'parent_occupation',
        'guardian_name',
        'guardian_occupation',
        'parent_status',
        'current_living_with',
        'user_class',
        'user_stream',
        'user_sub_class',
    )
    verbose_name = 'User Agency Information'
    verbose_name_plural = 'User Agency Details'


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'id', 'email', 'role',
                    'active_agency_name', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'is_gyalsung')
    search_fields = ('username', 'email', 'identity_number', 'role')
    ordering = ('username',)

    # Define fieldsets for add/edit views
    fieldsets = (
        (None, {'fields': ('username', 'email',
         'password', 'identity_number', 'nationality')}),
        ('Personal Information', {
            'fields': (
                'first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender',
                'mob_number', 'father_name', 'mother_name',
            )
        }),
        ('Address', {
            'fields': (
                'perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag',
                'ps_add_village', 'ps_add_gewog', 'ps_add_dzongkhag',
            )
        }),
        ('Agency and Role', {
            'fields': ('role', 'active_agency', 'access_level', 'is_gyalsung', 'academy_code')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser')
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Add fieldsets specifically for add_view, if needed
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'active_agency', 'role')
        }),
    )

    # Inline class to add UserAgency information
    inlines = [UserAgencyInline]

    def get_form(self, request, obj=None, **kwargs):
        # Ensure active_agency is available in the form
        form = super().get_form(request, obj, **kwargs)
        if 'active_agency' in form.base_fields:
            form.base_fields['active_agency'].queryset = Agency.objects.all()
        return form

    def active_agency_name(self, obj):
        return obj.active_agency.agency_name if obj.active_agency else "Not assigned"
    active_agency_name.short_description = "Active Agency"


admin.site.register(CustomUser, CustomUserAdmin)


class PreRecordedUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'identity_number',
                    'is_registered', 'agency_name')
    list_filter = ('is_registered', 'role')
    search_fields = ('username', 'email', 'identity_number')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'identity_number', 'nationality')}),
        ('Personal Information', {
            'fields': (
                'first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender',
                'mob_number', 'father_name', 'mother_name',
            )
        }),
        ('Address', {
            'fields': (
                'perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag',
                'ps_add_village', 'ps_add_gewog', 'ps_add_dzongkhag',
            )
        }),
        ('Agency and Registration', {
            'fields': (
                'role', 'access_level', 'is_gyalsung', 'academy_code', 'is_registered',
                'agency_name', 'agency_code',
            )
        }),
    )


admin.site.register(PreRecordedUser, PreRecordedUserAdmin)


class AgencyAdmin(admin.ModelAdmin):
    list_display = ('agency_code', 'agency_name', 'present_dzongkhag')
    search_fields = ('agency_code', 'agency_name')


admin.site.register(Agency, AgencyAdmin)
