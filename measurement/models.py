from django.db import models
from access.models import CustomUser 
from django.utils import timezone  # Import timezone module

class Submission(models.Model):
    test_type_name = models.CharField(max_length=100)
    question_set_name = models.CharField(max_length=100)
    question = models.TextField()
    answer = models.TextField()
    diagnosis = models.TextField()
    substance = models.CharField(max_length=100)
    specify = models.TextField()
    score = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)  # 'created_at' field for Submission model

class Diagnosis(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    gad_diagnosis = models.TextField()
    gad_flag = models.CharField(max_length=10, choices=[('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    phq_diagnosis = models.TextField()
    phq_flag = models.CharField(max_length=10, choices=[('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    assist_diagnosis = models.TextField()
    assist_flag = models.CharField(max_length=10, choices=[('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    school_env = models.TextField()
    overall_flag = models.CharField(max_length=10, choices=[('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    created_at = models.DateTimeField(default=timezone.now)  # 'created_at' field for Diagnosis model
