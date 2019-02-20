from django.urls import path
from .views import UserCreate, UserList, LoginView, PasswordResetRequestView, PasswordResetView, GetUserDetailsView, UpdateGyalsungDetails, UpdateUserInfoView
from . import views

urlpatterns = [
    # Authentication
    path('register/', UserCreate.as_view(), name='user-register'),
    path('users/', UserList.as_view(), name='user-list'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset-request/', PasswordResetRequestView.as_view(),
         name='password-reset-request'),
    path('password-reset/<str:token>/',
         PasswordResetView.as_view(), name='password-reset'),
    path('register-user/', views.register_user, name='register_user'),
    path('verify-pre-recorded-user/', views.verify_pre_recorded_user,
         name='verify_pre_recorded_user'),
    path('register-pre-recorded-user/', views. register_pre_recorded_user,
         name=' register_pre_recorded_user'),
    path('get-user-details/', GetUserDetailsView.as_view(), name='get_user_details'),
    path('user-logout/', views.user_logout, name='user_logout'),
    path('update-gyalsung-user/<int:pk>/',
         UpdateGyalsungDetails.as_view(), name='update_gyalsung_details'),

    path('get_csrf_token/', views.get_csrf_token, name='get_csrf_token'),

    # API CALLS
    path('get-citizen-details/<str:cid>/',
         views.fetch_citizen_details, name='get_citizen_details'),
    path('verify-pre-recorded-user/', views.verify_pre_recorded_user,
         name='verify-pre-recorded-user'),
    path('get-rcsc-details/<str:cid>/',
         views.fetch_rcsc_details, name='get_rcsc_details'),
    path('get-rcsc-details/<str:cid>/<str:reg_email>/',
         views.fetch_rcsc_details, name='get_rcsc_details_with_email'),
    path('get-emis-student-details/<str:student_code>/<str:dob>/<str:reg_email>/',
         views.get_emis_student_details, name='get_emis_student_details'),
    path('get-emis-staff-details/<str:emp_id>/<str:reg_email>/',
         views.get_emis_staff_details, name='get_emis_staff_details'),
    path('update-user-info/', UpdateUserInfoView.as_view(), name='update-user-info'),
]
