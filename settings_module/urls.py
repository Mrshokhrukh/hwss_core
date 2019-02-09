from django.urls import path
from .views import AppConfigListView

urlpatterns = [
    path('', AppConfigListView.as_view(), name='appconfig-list'),
]
