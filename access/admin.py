from django.contrib import admin
from .models import CustomUser, Agency, UserAgency

class UserAgencyInline(admin.TabularInline):
    model = UserAgency

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'active_agency')
    inlines = [UserAgencyInline]

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'role', 'active_agency'),
        }),
        ('Personal Information', {
            'fields': ('first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender', 'identity_number', 'nationality', 'mob_number', 'father_name', 'mother_name'),
        }),
        ('Address Information', {
            'fields': ('perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag'),
        }),
        ('Gyalsuung Information', {
            'fields': ('is_gyalsung', 'academy_code'),
        }),
    )

    def active_agency(self, obj):
        try:
            active_agency = obj.agency.filter(is_active=True).first()
            return active_agency.agency_name if active_agency else None
        except AttributeError:
            return None

    active_agency.short_description = 'Active Agency'


class AgencyAdmin(admin.ModelAdmin):
    list_display = ('agency_name',)
    inlines = [UserAgencyInline]

class UserAgencyAdmin(admin.ModelAdmin):
    list_display = ('user', 'agency', 'get_is_active')

    def get_is_active(self, obj):
        return obj.user.is_active if obj.user else False  # Check if the associated user is active
    get_is_active.short_description = 'Is Active'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(UserAgency, UserAgencyAdmin)
