from django.contrib import admin
from .models import ActiveUser, LifetimeUser, UserSubmission, Submission, Measurement, MeasurementAssist, MeasurementSubstance, TestType, QuestionSet
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from access.models import CustomUser

class SubmissionInline(admin.StackedInline):
    model = Submission
    extra = 1
    readonly_fields = ['question', 'answer', 'score', 'substance', 'specify', 'diagnosis', 'created_at']  # Add readonly fields

class MeasurementInline(admin.StackedInline):
    model = Measurement
    extra = 1
    readonly_fields = ['gad_measurement', 'gad_flag', 'phq_measurement', 'phq_flag', 'suicidal_measurement', 'suicidal_flag', 'ace_measurement', 'ace_flag', 'overall_flag', 'created_at']  # Add readonly fields

class MeasurementAssistInline(admin.StackedInline):
    model = MeasurementAssist
    extra = 1
    readonly_fields = ['alcoholic_measurement', 'alcoholic_flag', 'tobacco_measurement', 'tobacco_flag', 'cannabis_measurement', 'cannabis_flag', 'cocaine_measurement', 'cocaine_flag', 'amphetamine_measurement', 'amphetamine_flag', 'inhalants_measurement', 'inhalants_flag', 'sedatives_measurement', 'sedatives_flag', 'hallucinogens_measurement', 'hallucinogens_flag', 'opioids_measurement', 'opioids_flag', 'other_measurement', 'other_flag', 'other_name', 'created_at']  # Add readonly fields

class TestTypeInline(admin.StackedInline):
    model = TestType
    extra = 1
    readonly_fields = ['name']  # Add readonly fields

class QuestionSetInline(admin.StackedInline):
    model = QuestionSet
    extra = 1
    readonly_fields = ['name']  # Add readonly fields


@admin.register(UserSubmission)
class UserSubmissionAdmin(admin.ModelAdmin):
    inlines = [SubmissionInline, MeasurementInline, MeasurementAssistInline, QuestionSetInline]
    list_display = ['user', 'created_at']

class CustomUserAdmin(BaseUserAdmin):
    inlines = [MeasurementAssistInline, MeasurementInline]

@admin.register(LifetimeUser)
class LifetimeUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_submission')
    list_filter = ('user_submission',)

@admin.register(ActiveUser)
class ActiveUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_submission')
    list_filter = ('user_submission',)

admin.site.site_header = "Your Admin Panel Header"
