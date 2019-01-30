from django.urls import path
from .views import UserCreate, UserList, LoginView, PasswordResetRequestView, PasswordResetView
from . import views

urlpatterns = [
    path('register/', UserCreate.as_view(), name='user-register'),
    path('users/', UserList.as_view(), name='user-list'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset-request/', PasswordResetRequestView.as_view(),
         name='password-reset-request'),
    path('password-reset/<str:token>/',
         PasswordResetView.as_view(), name='password-reset'),
    path('get-citizen-details/<str:cid>/',
         views.fetch_citizen_details, name='get_citizen_details'),
    path('verify-pre-recorded-user/', views.verify_pre_recorded_user,
         name='verify-pre-recorded-user'),
    path('get-rcsc-details/<str:cid>/',
         views.fetch_rcsc_details, name='get_rcsc_details'),
    path('get-emis-student/<str:student_id>/<str:reg_email>/<str:dob>/', views.fetch_emis_student_details, name='fetch_emis_student_details'),
    path('get-emis-employee/<str:employee_id>/<str:reg_email>/', views.fetch_emis_employee_details, name='fetch_emis_employee_details'),
    path('get-rcsc-details/<str:cid>/<str:reg_email>/',
         views.fetch_rcsc_details, name='get_rcsc_details_with_email'),
    path('register-user/', views.register_user, name='register_user'),
    path('register-agency/', views.register_agency, name='register_agency'),
    path('verify-pre-recorded-user/', views.verify_pre_recorded_user,
         name='verify_pre_recorded_user'),
    path('register-pre-recorded-user/', views. register_pre_recorded_user,
         name=' register_pre_recorded_user'),
    path('register-pre-recorded-agency/', views.register_pre_recorded_agency,
         name='register_pre_recorded_agency'),
    path('get-user-details/', views.get_user_details, name='get_user_details'),
    path('user-logout/', views.user_logout, name='user_logout'),


]
