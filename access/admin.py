from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Agency, PreRecordedUser, PreRecordedAgency


class PreRecordedAgencyInline(admin.StackedInline):
    model = PreRecordedAgency
    extra = 0  # Prevents displaying empty new agency form by default
    can_delete = True  # Allows deleting agencies if needed


@admin.register(PreRecordedUser)
class PreRecordedUserAdmin(admin.ModelAdmin):
    list_display = ('identity_number', 'first_name', 'last_name', 'email', 'date_joined')
    search_fields = ('identity_number', 'first_name', 'last_name', 'email')
    ordering = ('date_joined',)
    readonly_fields = ('date_joined',)
    inlines = [PreRecordedAgencyInline]


class AgencyInline(admin.StackedInline):
    model = Agency
    can_delete = False
    verbose_name_plural = 'Agency'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    inlines = (AgencyInline, )
    list_display = ('email', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')  # Change 'email' to 'username'
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email','username', 'first_name', 'last_name', 'email')  # Change 'email' to 'username'
    ordering = ('username',)  # Change 'email' to 'username'
    filter_horizontal = ('groups', 'user_permissions',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # Change 'email' to 'username'
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'identity_number', 'nationality', 'date_of_birth', 'gender', 'mob_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Custom fields'), {'fields': ('is_gyalsung', 'perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'identity_number', 'nationality', 'date_of_birth', 'gender', 'mob_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Custom fields'), {'fields': ('is_gyalsung', 'perm_add_village', 'perm_add_gewog', 'perm_add_dzongkhag')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
