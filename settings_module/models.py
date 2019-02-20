from django.db import models
from django.utils.html import format_html

class AppConfig(models.Model):
    login_logo = models.ImageField(upload_to='logos/')
    registration_logo = models.ImageField(upload_to='logos/')
    landing_page_logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    landing_img_bg = models.ImageField(upload_to='logos/', null=True, blank=True)
    landing_tag_line = models.CharField(max_length=255, null=True, blank=True)
    dashboard_logo = models.ImageField(upload_to='logos/')
    carousel_image_1 = models.ImageField(upload_to='carousel/', null=True, blank=True)
    carousel_image_2 = models.ImageField(upload_to='carousel/', null=True, blank=True)
    carousel_image_3 = models.ImageField(upload_to='carousel/', null=True, blank=True)
    carousel_image_4 = models.ImageField(upload_to='carousel/', null=True, blank=True)
    app_name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=255)
    helpline_number_1 = models.CharField(max_length=20)
    helpline_number_2 = models.CharField(max_length=20)
    response_service_logo = models.ImageField(upload_to='logos/')
    cluster_test_title = models.CharField(max_length=50, null=True, blank=True)
    cluster_test_content = models.TextField(max_length=500, null=True, blank=True)
    cluster_test_disclaimer = models.TextField(max_length=500, null=True, blank=True)
    cluster_test_icon = models.ImageField(upload_to='icons/', null=True, blank=True)
    copyright_message = models.CharField(max_length=255, null=True, blank=True)
    google_play_link = models.CharField(max_length=255, null=True, blank=True)
    apple_appstore_link = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return self.app_name
    
    def login_logo_preview(self):
        if self.login_logo:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', self.login_logo.url)
        else:
            return 'No Image'

    def registration_logo_preview(self):
        if self.registration_logo:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', self.registration_logo.url)
        else:
            return 'No Image'

    def landing_page_logo_preview(self):
        if self.landing_page_logo:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', self.landing_page_logo.url)
        else:
            return 'No Image'

    def dashboard_logo_preview(self):
        if self.dashboard_logo:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', self.dashboard_logo.url)
        else:
            return 'No Image'

    def response_service_logo_preview(self):
        if self.response_service_logo:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', self.response_service_logo.url)
        else:
            return 'No Image'

    def cluster_test_icon_preview(self):
        if self.response_service_logo:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', self.cluster_test_icon.url)
        else:
            return 'No Image'


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    route = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=100)
    roles = models.ManyToManyField('auth.Group', related_name='menu_items')

    def __str__(self):
        return self.name