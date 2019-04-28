from django.urls import path
from .views import SaveGyalsungUsers

urlpatterns = [
    path('save-gyalsung-users/', SaveGyalsungUsers.as_view(), name='save_gyalsung_users')
]
