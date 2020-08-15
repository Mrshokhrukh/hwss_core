from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Agency, UserAgency, PreRecordedUser

# Inline for UserAgency to be displayed within the CustomUser admin page.
# This allows for editing the user's agency details directly from the user page.
class UserAgencyInline(admin.StackedInline):
    """
    Makes the UserAgency model editable directly from the CustomUser admin page.
    This provides a convenient way to manage a user's relationship with an agency.
    """
    model = UserAgency
    can_delete = False  # We don't want to delete the agency relationship from here
    verbose_name_plural = 'Agency Details'
    fk_name = 'user'
    # Define fieldsets to organize the inline form
    fieldsets = (
        (None, {
            'fields': ('agency', 'user_code', 'user_role_agency')
        }),
        ('Educational Information', {
            'classes': ('collapse',), # This section will be collapsible
            'fields': ('user_class', 'user_stream', 'user_sub_class')
        }),
        ('Family Information', {
            'classes': ('collapse',),
            'fields': ('parent_occupation', 'guardian_name', 'guardian_occupation', 'parent_status', 'current_living_with')
        }),
    )


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the CustomUser model.
    Extends the default UserAdmin to include custom fields and an inline for UserAgency.
    """
    inlines = (UserAgencyInline,)
    
    # Use fieldsets to structure the user creation/edit form in the admin panel.
    # This provides a more organized and user-friendly interface.
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'middle_name', 'last_name', 'email', 'date_of_birth', 'gender', 'identity_number', 'nationality', 'mob_number')}),
        ('Permissions & Role', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'role', 'access_level')}),
        ('Agency Information', {'fields': ('active_agency',)}),
        ('Address Information', {
            'classes': ('collapse',),
            'fields': ('perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag', 'ps_add_village', 'ps_add_gewog', 'ps_add_dzongkhag')
        }),
        ('Family Details', {
            'classes': ('collapse',),
            'fields': ('father_name', 'mother_name')
        }),
        ('Additional Info', {
            'classes': ('collapse',),
            'fields': ('profile_picture', 'is_gyalsung', 'academy_code', 'is_old_case_user', 'registration_method')
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to display in the main list view of users.
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    
    # Fields that can be used to filter the user list.
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'role')
    
    # Fields that can be searched.
    search_fields = ('username', 'first_name', 'last_name', 'email', 'identity_number')
    
    # Default ordering for the user list.
    ordering = ('username',)
    
    # Add a filter for horizontal or vertical display of many-to-many fields (e.g., groups).
    filter_horizontal = ('groups', 'user_permissions',)

    # When saving a user from the admin, this ensures the inline is saved correctly.
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Agency model.
    Provides an independent section to manage agencies.
    """
    list_display = ('agency_name', 'agency_code', 'agency_parent', 'present_dzongkhag')
    search_fields = ('agency_name', 'agency_code', 'agency_parent')
    list_filter = ('present_dzongkhag', 'present_gewog')
    ordering = ('agency_name',)


@admin.register(UserAgency)
class UserAgencyAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserAgency model.
    Provides an independent section to view and manage all user-agency relationships.
    """
    list_display = ('user', 'agency', 'user_role_agency', 'user_class')
    search_fields = ('user__username', 'user__email', 'agency__agency_name', 'user_code')
    list_filter = ('agency', 'user_role_agency', 'user_class', 'user_stream')
    # Use autocomplete_fields for better performance and UI with foreign keys.
    autocomplete_fields = ['user', 'agency']
    ordering = ('user',)


@admin.register(PreRecordedUser)
class PreRecordedUserAdmin(admin.ModelAdmin):
    """
    Admin configuration for the PreRecordedUser model.
    This is for users who are in the system but have not yet registered.
    """
    list_display = ('identity_number', 'first_name', 'last_name', 'email', 'agency_name', 'is_registered')
    search_fields = ('identity_number', 'first_name', 'last_name', 'email', 'agency_name', 'agency_code')
    list_filter = ('is_registered', 'agency_name')
    ordering = ('first_name', 'last_name')
    
    # Making fields read-only might be useful if this data is imported and not meant to be edited.
    # readonly_fields = ('date_joined',)
