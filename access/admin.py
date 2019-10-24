from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser, Agency, UserAgency, PreRecordedUser


class UserAgencyInline(admin.TabularInline):
    model = UserAgency
    extra = 1
    readonly_fields = ['agency', 'user_code']


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active',
                    'is_staff', 'date_joined', 'agency_display')
    list_filter = ('role', 'is_active', 'is_staff',
                   'is_gyalsung', 'date_joined')
    search_fields = ('username', 'email', 'first_name',
                     'last_name', 'identity_number')
    readonly_fields = ('date_joined',)
    inlines = [UserAgencyInline]

    def agency_display(self, obj):
        return obj.active_agency.agency_name if obj.active_agency else '-'
    agency_display.short_description = 'Agency'


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('agency_code', 'agency_name',
                    'present_dzongkhag', 'present_gewog', 'present_village')
    search_fields = ('agency_code', 'agency_name',
                     'present_dzongkhag', 'present_gewog', 'present_village')


@admin.register(UserAgency)
class UserAgencyAdmin(admin.ModelAdmin):
    list_display = ('user', 'agency', 'user_code',
                    'parent_occupation', 'user_role_agency')
    search_fields = ('user__email', 'agency__agency_name',
                     'user_code', 'user_role_agency')


@admin.register(PreRecordedUser)
class PreRecordedUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'identity_number',
                    'is_registered', 'role', 'agency_name', 'date_joined')
    list_filter = ('role', 'is_registered', 'is_gyalsung', 'date_joined')
    search_fields = ('username', 'email', 'identity_number',
                     'first_name', 'last_name')
    readonly_fields = ('date_joined',)

    def agency_display(self, obj):
        return obj.agency_name or '-'
    agency_display.short_description = 'Agency'


# Registering models
# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Agency, AgencyAdmin)
# admin.site.register(UserAgency, UserAgencyAdmin)
# admin.site.register(PreRecordedUser, PreRecordedUserAdmin)
