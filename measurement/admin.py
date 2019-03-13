from django.contrib import admin
from .models import UserSubmission, TestType, QuestionSet, Submission, Diagnosis

class SubmissionInline(admin.StackedInline):
    model = Submission
    extra = 0
    readonly_fields = ['created_at']
    can_delete = False

class QuestionSetInline(admin.StackedInline):
    model = QuestionSet
    extra = 0

class TestTypeInline(admin.StackedInline):
    model = TestType
    extra = 0

class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
    inlines = [SubmissionInline, QuestionSetInline, TestTypeInline]

admin.site.register(UserSubmission, UserSubmissionAdmin)


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['user_submission', 'question', 'answer', 'diagnosis', 'substance', 'specify', 'score', 'question_set', 'created_at']
    search_fields = ['user_submission__user__username', 'question', 'answer', 'diagnosis', 'substance', 'specify', 'question_set__name']
    readonly_fields = ['created_at']
    list_filter = ['user_submission__user']

admin.site.register(Submission, SubmissionAdmin)
