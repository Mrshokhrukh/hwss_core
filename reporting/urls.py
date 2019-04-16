from django.urls import path
from .views import orchestrate_reporting, update_user_archive

urlpatterns = [
    path('generate-report/', orchestrate_reporting, name='orchestrate_reporting'),
    path('update-user-archive/', update_user_archive, name='update_user_archive'),
]
