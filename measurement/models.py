from django.db import models
from access.models import CustomUser
from django.utils import timezone


class UserSubmission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    test_type_name = models.CharField(
        max_length=100, null=True, blank=True)  # Add this field
    created_at = models.DateTimeField(
        default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}'


class TestType(models.Model):
    name = models.CharField(max_length=100)
    user_submission = models.ForeignKey(
        UserSubmission, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class QuestionSet(models.Model):
    name = models.CharField(max_length=100)
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE)
    user_submission = models.ForeignKey(
        UserSubmission, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Submission(models.Model):
    user_submission = models.ForeignKey(
        UserSubmission, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    diagnosis = models.TextField(null=True, blank=True)
    substance = models.CharField(max_length=100)
    specify = models.TextField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    question_set = models.ForeignKey(
        QuestionSet, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(
        default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f'Submission for {self.user_submission.user.username}'


class Diagnosis(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gad_diagnosis = models.TextField()
    gad_flag = models.CharField(max_length=10, choices=[
        ('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    phq_diagnosis = models.TextField()
    phq_flag = models.CharField(max_length=10, choices=[
        ('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    assist_diagnosis = models.TextField()
    assist_flag = models.CharField(max_length=10, choices=[
        ('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    school_env = models.TextField()
    overall_flag = models.CharField(max_length=10, choices=[
        ('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    created_at = models.DateTimeField(
        default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f'Diagnosis for {self.user.username}'
