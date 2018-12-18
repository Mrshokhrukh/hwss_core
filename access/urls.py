from django.urls import path
from .views import UserCreate, UserList, LoginView, PasswordResetRequestView, PasswordResetView, CitizenDetailsView

urlpatterns = [
    path('register/', UserCreate.as_view(), name='user-register'),
    path('users/', UserList.as_view(), name='user-list'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/<str:token>/', PasswordResetView.as_view(), name='password-reset'),
    path('get-citizen-details/', CitizenDetailsView.as_view(), name='get-citizen-details'),
]
