from django.urls import path
from .views import orchestrate_reporting, get_all_users_data

urlpatterns = [
    path('generate-report/', orchestrate_reporting, name='orchestrate_reporting'),
    path('get-all-user-data/', get_all_users_data, name='get_all_user_data'),
]
