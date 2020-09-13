from django.contrib import admin

from gyalsung_users.models import GyalsungUserProfile


class GyalsungUserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "full_name",
        "gender",
        "dob",
        "mobile_number",
        "ps_add_dzongkhag",
        "academy_code",
        "batch_number",
    )
    list_filter = ("gender", "ps_add_dzongkhag", "academy_code")
    search_fields = (
        "username",
        "full_name",
        "mobile_number",
        "ps_add_dzongkhag",
        "academy_code",
    )


admin.site.register(GyalsungUserProfile, GyalsungUserProfileAdmin)
