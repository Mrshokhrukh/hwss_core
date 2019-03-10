from django.contrib import admin
from .models import Submission, Diagnosis

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('test_type_name', 'question_set_name', 'user', 'created_at')
    search_fields = ('test_type_name', 'question_set_name', 'user__username')
    list_filter = ('test_type_name', 'question_set_name', 'created_at')  # Corrected 'list_filter'
    readonly_fields = ('created_at',)  # Corrected 'readonly_fields'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('user', 'gad_diagnosis', 'phq_diagnosis', 'assist_diagnosis')
    search_fields = ('user__username',)
    list_filter = ('gad_diagnosis', 'phq_diagnosis', 'assist_diagnosis')
