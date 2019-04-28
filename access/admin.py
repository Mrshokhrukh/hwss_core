from asyncio import format_helpers
from django.utils.html import format_html
import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import CustomUser, Agency, UserAgency, PreRecordedUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from import_export.admin import ImportExportModelAdmin


class UserAgencyInline(admin.TabularInline):
    model = UserAgency

# just a test for test


class PreRecordedUserAdmin(ImportExportModelAdmin):
    list_display = ('identity_number', 'first_name', 'last_name',
                    'date_of_birth', 'gender', 'is_registered')
    search_fields = ['identity_number', 'first_name', 'last_name']
    list_filter = ['is_registered']
    ordering = ['identity_number']
    actions = ['mark_as_registered']

    def mark_as_registered(self, request, queryset):
        queryset.update(is_registered=True)
    mark_as_registered.short_description = "Mark selected users as registered"


class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'username', 'email', 'role',
                    'active_agency', 'display_profile_picture')
    inlines = [UserAgencyInline]

    fieldsets = (
        (None, {
            # Include password field here
            'fields': ('username', 'email', 'role', 'active_agency', 'password'),
        }),
        ('Personal Information', {
            'fields': ('first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender', 'identity_number', 'nationality', 'mob_number', 'father_name', 'mother_name'),
        }),
        ('Address Information', {
            'fields': ('perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag', 'ps_add_village', 'ps_add_gewog', 'ps_add_dzongkhag'),
        }),
        ('Gyalsuung Information', {
            'fields': ('is_gyalsung', 'academy_code'),
        }),
        ('Profile Picture', {
            'fields': ('profile_picture',),
        }),
    )

    def active_agency(self, obj):
        try:
            active_agency = obj.agency.filter(is_active=True).first()
            return active_agency.agency_name if active_agency else None
        except AttributeError:
            return None

    def display_profile_picture(self, obj):
        return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />'.format(obj.profile_picture.url)) if obj.profile_picture else None
    display_profile_picture.short_description = 'Profile Picture'


class AgencyAdmin(admin.ModelAdmin):
    list_display = ('agency_name',)
    inlines = [UserAgencyInline]


class UserAgencyAdmin(admin.ModelAdmin):
    list_display = ('user', 'agency', 'get_is_active')

    def get_is_active(self, obj):
        # Check if the associated user is active
        return obj.user.is_active if obj.user else False
    get_is_active.short_description = 'Is Active'


admin.site.register(PreRecordedUser, PreRecordedUserAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(UserAgency, UserAgencyAdmin)
