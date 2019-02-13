from django.contrib import admin
from .models import AppConfig

class AppConfigAdmin(admin.ModelAdmin):
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
        ('Cluster Test Information', {
            'fields': ('cluster_test_title', 'cluster_test_content', 'cluster_test_disclaimer', 'cluster_test_icon',)
        }),
        ('Copyright Information', {
            'fields': ('copyright_message',)  # Add the copyright_message field here
        }),
    )
    list_display = ('app_name', 'tagline', 'show_login_logo', 'show_registration_logo',
                    'show_landing_page_logo', 'show_dashboard_logo', 'show_response_service_logo',
                    'copyright_message')  # Add copyright_message
    search_fields = ('app_name', 'tagline',)

    def show_login_logo(self, obj):
        return obj.login_logo_preview()
    show_login_logo.short_description = 'Login Logo'

    def show_registration_logo(self, obj):
        return obj.registration_logo_preview()
    show_registration_logo.short_description = 'Registration Logo'

    def show_landing_page_logo(self, obj):
        return obj.landing_page_logo_preview()
    show_landing_page_logo.short_description = 'Landing Page Logo'

    def show_dashboard_logo(self, obj):
        return obj.dashboard_logo_preview()
    show_dashboard_logo.short_description = 'Dashboard Logo'

    def show_response_service_logo(self, obj):
        return obj.response_service_logo_preview()
    show_response_service_logo.short_description = 'Response Service Logo'

admin.site.register(AppConfig, AppConfigAdmin)
