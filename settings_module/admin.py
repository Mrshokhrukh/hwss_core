from django import forms
from django.contrib import admin
from django_quill.forms import QuillFormField

from settings_module.models import AppConfig, MenuItem, Video


class AppConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Logos",
            {
                "fields": (
                    "login_logo",
                    "registration_logo",
                    "landing_page_logo",
                    "dashboard_logo",
                    "landing_img_bg",
                )
            },
        ),
        (
            "Carousel Images",
            {
                "fields": (
                    "carousel_image_1",
                    "carousel_image_2",
                    "carousel_image_3",
                    "carousel_image_4",
                )
            },
        ),
        (
            "Application Information",
            {
                "fields": (
                    "app_name",
                    "tagline",
                    "helpline_number_1",
                    "helpline_number_2",
                    "response_service_logo",
                    "landing_tag_line",
                )
            },
        ),
        (
            "Cluster Test Information",
            {
                "fields": (
                    "cluster_test_title",
                    "cluster_test_content",
                    "cluster_test_disclaimer",
                    "cluster_test_icon",
                )
            },
        ),
        (
            "Copyright Information",
            {
                "fields": ("copyright_message",),
            },
        ),
        (
            "Mobile App Store Links",
            {
                "fields": (
                    "google_play_link",
                    "apple_appstore_link",
                )
            },
        ),
    )
    list_display = (
        "app_name",
        "tagline",
        "show_login_logo",
        "show_registration_logo",
        "show_landing_page_logo",
        "show_dashboard_logo",
        "show_response_service_logo",
        "copyright_message",
    )  # Add copyright_message
    search_fields = (
        "app_name",
        "tagline",
    )

    def show_login_logo(self, obj):
        return obj.login_logo_preview()

    show_login_logo.short_description = "Login Logo"

    def show_registration_logo(self, obj):
        return obj.registration_logo_preview()

    show_registration_logo.short_description = "Registration Logo"

    def show_landing_page_logo(self, obj):
        return obj.landing_page_logo_preview()

    show_landing_page_logo.short_description = "Landing Page Logo"

    def show_dashboard_logo(self, obj):
        return obj.dashboard_logo_preview()

    show_dashboard_logo.short_description = "Dashboard Logo"

    def show_response_service_logo(self, obj):
        return obj.response_service_logo_preview()

    show_response_service_logo.short_description = "Response Service Logo"


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "route", "icon_class", "list_roles")
    search_fields = ("name", "route")
    filter_horizontal = ("roles",)

    def list_roles(self, obj):
        return ", ".join([role.name for role in obj.roles.all()])

    list_roles.short_description = "Roles"


class VideoForm(forms.ModelForm):
    description = QuillFormField()

    class Meta:
        model = Video
        fields = "__all__"


class VideoAdmin(admin.ModelAdmin):
    form = VideoForm
    list_display = (
        "title",
        "topic",
        "description",
        "video_link",
        "video_file",
        "video_for",
    )
    search_fields = ["title", "topic"]
    list_filter = ["topic", "video_for"]


admin.site.register(AppConfig, AppConfigAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Video, VideoAdmin)
