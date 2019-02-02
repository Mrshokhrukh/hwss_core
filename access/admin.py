from django.contrib import admin
from .models import CustomUser, Agency, PreRecordedUser, PreRecordedAgency, UserAgency


class UserAgencyInline(admin.TabularInline):
    model = UserAgency
    extra = 0
    verbose_name = 'Active Agency'
    verbose_name_plural = 'Active Agencies'


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'first_name', 'last_name',
                    'is_staff', 'is_active', 'get_active_agency')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'identity_number',
         'nationality', 'date_of_birth', 'gender', 'mob_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom fields', {'fields': (
            'is_gyalsung', 'perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Personal info', {'fields': ('first_name', 'last_name', 'identity_number',
         'nationality', 'date_of_birth', 'gender', 'mob_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Custom fields', {'fields': (
            'is_gyalsung', 'perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag')}),
    )
    inlines = [UserAgencyInline]

    def get_active_agency(self, obj):
        active_user_agency = obj.useragency_set.filter(is_active=True).first()
        if active_user_agency:
            return active_user_agency.agency.agency_name
        return None


    get_active_agency.short_description = 'Active Agency'
    get_active_agency.admin_order_field = 'useragency__is_active'


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    model = Agency
    list_display = ('agency_code', 'agency_name', 'status')
    search_fields = ('agency_code', 'agency_name')
    inlines = [UserAgencyInline]
