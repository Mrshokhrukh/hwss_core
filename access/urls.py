from django.urls import path

from .views import (
    CustomTokenAuthentication,
    GetUserDetailsView,
    LoginGyalsung,
    LoginView,
    PasswordResetRequestView,
    PasswordResetView,
    UpdateGyalsungDetails,
    UserCreate,
    UserList,
    change_password,
    check_email_cid,
    fetch_citizen_details,
    fetch_rcsc_details,
    get_csrf_token,
    get_emis_staff_details,
    get_emis_student_details,
    get_referral_counselors,
    get_gyalsung_user_data_using_cid,
    register_pre_recorded_user,
    register_gyalsung_user_using_cid,
    register_user,
    registerCounselorCaseUser,
    registerCounselorEventUser,
    update_user_info,
    user_logout,
    verify_pre_recorded_user,
)

urlpatterns = [
    # Authentication
    path("register/", UserCreate.as_view(), name="user-register"),
    path("users/", UserList.as_view(), name="user-list"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "password-reset-request/",
        PasswordResetRequestView.as_view(),
        name="password-reset-request",
    ),
    path(
        "password-reset/<str:token>/",
        PasswordResetView.as_view(),
        name="password-reset",
    ),
    path("register-user/", register_user, name="register_user"),
    path(
        "register-counselor-event-user/",
        registerCounselorEventUser,
        name="register_counselor_event_user",
    ),
    path(
        "register-counselor-case-user/",
        registerCounselorCaseUser,
        name="register_counselor_case_user",
    ),
    path(
        "register-pre-recorded-user/",
        register_pre_recorded_user,
        name="register_pre_recorded_user",
    ),
    path(
        "register-gyalsung-user/",
        register_gyalsung_user_using_cid,
        name="register_gyalsung_user",
    ),
    path(
        "get-gyalsung-user-data/",
        get_gyalsung_user_data_using_cid,
        name="get_gyalsung_user_data",
    ),
    path("get-user-details/", GetUserDetailsView.as_view(), name="get_user_details"),
    path("user-logout/", user_logout, name="user_logout"),
    path(
        "update-gyalsung-user/",
        UpdateGyalsungDetails.as_view(),
        name="update_gyalsung_details",
    ),
    path("get_csrf_token/", get_csrf_token, name="get_csrf_token"),
    path(
        "get-referral-counselors/",
        get_referral_counselors,
        name="get_referral_counselors",
    ),
    # API CALLS
    path(
        "get-citizen-details/<str:cid>/",
        fetch_citizen_details,
        name="get_citizen_details",
    ),
    path(
        "verify-pre-recorded-user/",
        verify_pre_recorded_user,
        name="verify-pre-recorded-user",
    ),
    path("get-rcsc-details/<str:cid>/", fetch_rcsc_details, name="get_rcsc_details"),
    path(
        "get-rcsc-details/<str:cid>/<str:reg_email>/",
        fetch_rcsc_details,
        name="get_rcsc_details_with_email",
    ),
    path(
        "get-emis-student-details/<str:student_code>/<str:dob>/<str:reg_email>/",
        get_emis_student_details,
        name="get_emis_student_details",
    ),
    path(
        "get-emis-staff-details/<str:emp_id>/<str:reg_email>/",
        get_emis_staff_details,
        name="get_emis_staff_details",
    ),
    path("update-user-info/", update_user_info, name="update_user_info"),
    path("change-password/", change_password, name="change_password"),
    path(
        "authenticate-token/",
        CustomTokenAuthentication.as_view(),
        name="authenticate-token",
    ),
    path("get-gyalsung-token/", LoginGyalsung.as_view(), name="login_gyalsung"),
    path("check_email_cid/", check_email_cid, name="check_email_cid"),
]
