from django.contrib import admin
from .models import AppConfig

class AppConfigAdmin(admin.ModelAdmin):
    # Define fieldsets to group related fields together
    fieldsets = (
        ('Logos', {
            'fields': ('login_logo', 'registration_logo', 'landing_page_logo', 'dashboard_logo',)
        }),
        ('Carousel Images', {
            'fields': ('carousel_image_1', 'carousel_image_2', 'carousel_image_3', 'carousel_image_4',)
        }),
        ('Application Information', {
            'fields': ('app_name', 'tagline', 'helpline_number_1', 'helpline_number_2', 'response_service_logo',)
        }),
    )
    # List of fields to be displayed on the admin list page
    list_display = ('app_name', 'tagline',)
    # Search fields for the admin list page
    search_fields = ('app_name', 'tagline',)

admin.site.register(AppConfig, AppConfigAdmin)
