from django.urls import path
from .views import AppConfigListView, MenuItemsAPIView, get_videos

urlpatterns = [
    path('appconfig/', AppConfigListView.as_view(), name='appconfig-list'),
    path('menuItem/', MenuItemsAPIView.as_view(),
         name='menu-item-list'),
    path('get-videos/', get_videos, name='get_videos'),
]
