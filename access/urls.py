from django.urls import path
from .views import UserCreate, UserList, LoginView, PasswordResetRequestView, PasswordResetView  
from . import views

urlpatterns = [
    path('register/', UserCreate.as_view(), name='user-register'),
    path('users/', UserList.as_view(), name='user-list'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/<str:token>/', PasswordResetView.as_view(), name='password-reset'),
    path('get-citizen-details/<str:cid>/', views.fetch_citizen_details, name='get_citizen_details'),
    path('verify-pre-recorded-user/', views.verify_pre_recorded_user, name='verify-pre-recorded-user'),
    path('get-rcsc-details/<str:cid>/', views.fetch_rcsc_details, name='get_rcsc_details'),

]
