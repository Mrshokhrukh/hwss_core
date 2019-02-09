from django.db import models

class AppConfig(models.Model):
    login_logo = models.ImageField(upload_to='logos/')
    registration_logo = models.ImageField(upload_to='logos/')
    landing_page_logo = models.ImageField(upload_to='logos/')
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

    def __str__(self):
        return self.app_name
