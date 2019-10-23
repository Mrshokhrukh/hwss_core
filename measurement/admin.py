from django.contrib import admin
from .models import (
    TestType, UserSubmission, QuestionSet, Submission, MeasurementSubstance,
    MeasurementAssist, Measurement, LifetimeUser, ActiveUser
)


class TestTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class QuestionSetInline(admin.TabularInline):
    model = QuestionSet
    extra = 1


# Removed SubmissionInline from this part
class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'test_type', 'created_at',
                    'rescreened', 'mark_as_safe', 'is_old_case')
    list_filter = ('test_type', 'created_at', 'rescreened',
                   'mark_as_safe', 'is_old_case')
    search_fields = ('user__username', 'test_type__name')
    inlines = [QuestionSetInline]  # Removed SubmissionInline from here
    readonly_fields = ('created_at',)


class LifetimeUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_submission')
    search_fields = ('user__username',)
    filter_horizontal = ('substances_used',)


class ActiveUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_submission')
    search_fields = ('user__username',)
    filter_horizontal = ('substances_used',)


class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('user', 'overall_flag', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)


admin.site.register(TestType, TestTypeAdmin)
admin.site.register(UserSubmission, UserSubmissionAdmin)
admin.site.register(LifetimeUser, LifetimeUserAdmin)
admin.site.register(ActiveUser, ActiveUserAdmin)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(MeasurementSubstance)
admin.site.register(MeasurementAssist)
