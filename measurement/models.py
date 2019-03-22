from django.db import models
from access.models import CustomUser
from django.utils import timezone


class TestType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserSubmission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    test_type = models.ForeignKey(
        TestType, on_delete=models.CASCADE, related_name='submissions')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        unique_string = f'{self.user.username}_{self.test_type.name}_{self.created_at.strftime("%Y-%m-%d_%H")}'
        return unique_string


class QuestionSet(models.Model):
    name = models.CharField(max_length=100)
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE)
    user_submission = models.ForeignKey(
        UserSubmission, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Submission(models.Model):
    user_submission = models.ForeignKey(
        UserSubmission, on_delete=models.CASCADE, related_name='submissions')
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    score = models.IntegerField(null=True, blank=True)
    substance = models.CharField(max_length=100)
    specify = models.CharField(max_length=100) 
    diagnosis = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Submission for {self.user_submission.user.username}'


# ------------------------------------------------
# Measurement related models from here and below
# ------------------------------------------------
class MeasurementSubstance(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MeasurementAssist(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='measurementassist')
    user_submission = models.ForeignKey(
        UserSubmission, on_delete=models.CASCADE)
    alcoholic_measurement = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('high risk', 'High Risk'), ('moderate risk', 'Moderate Risk'), ('no risk', 'No Risk')])
    alcoholic_flag = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    tobacco_measurement = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('high risk', 'High Risk'), ('moderate risk', 'Moderate Risk'), ('no risk', 'No Risk')])
    tobacco_flag = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    cannabis_measurement = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('high risk', 'High Risk'), ('moderate risk', 'Moderate Risk'), ('no risk', 'No Risk')])
    cannabis_flag = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    cocaine_measurement = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('high risk', 'High Risk'), ('moderate risk', 'Moderate Risk'), ('no risk', 'No Risk')])
    cocaine_flag = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    amphetamine_measurement = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('high risk', 'High Risk'), ('moderate risk', 'Moderate Risk'), ('no risk', 'No Risk')])
    amphetamine_flag = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    inhalants_measurement = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('high risk', 'High Risk'), ('moderate risk', 'Moderate Risk'), ('no risk', 'No Risk')])
    inhalants_flag = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    sedatives_measurement = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('high risk', 'High Risk'), ('moderate risk', 'Moderate Risk'), ('no risk', 'No Risk')])
    sedatives_flag = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    hallucinogens_measurement = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('high risk', 'High Risk'), ('moderate risk', 'Moderate Risk'), ('no risk', 'No Risk')])
    hallucinogens_flag = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    opioids_measurement = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('high risk', 'High Risk'), ('moderate risk', 'Moderate Risk'), ('no risk', 'No Risk')])
    opioids_flag = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    other_measurement = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('high risk', 'High Risk'), ('moderate risk', 'Moderate Risk'), ('no risk', 'No Risk')])
    other_flag = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    other_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(
        default=timezone.now)

    def __str__(self):
        return f'MeasurementAssist data for {self.user.username}'


class Measurement(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='measurement')
    user_submission = models.ForeignKey(
        UserSubmission, on_delete=models.CASCADE)
    gad_measurement = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('severe', 'Severe'), ('moderate', 'Moderate'), ('mild', 'Mild'), ('minimal', 'Minimal')])
    gad_flag = models.CharField(max_length=10, blank=True, null=True, choices=[
        ('red', 'Red'), ('yellow', 'Yellow'), ('blue', 'Blue'), ('green', 'Green')])
    phq_measurement = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('severe', 'Severe'), ('moderately severe', 'Moderately Severe'), ('moderate', 'Moderate'), ('mild', 'Mild'), ('minimal', 'Minimal')])
    phq_flag = models.CharField(max_length=10, blank=True, null=True, choices=[
        ('red', 'Red'), ('orange', 'Orange'), ('yellow', 'Yellow'), ('blue', 'Blue'), ('green', 'Green')])
    suicidal_measurement = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('nearly everyday', 'Nearly every day'), ('more than half the days', 'More than half the days'), ('several days', 'Several days')])
    suicidal_flag = models.CharField(max_length=10, blank=True, null=True, choices=[
        ('red', 'Red'), ('orange', 'Orange'), ('yellow', 'Yellow')])
    ace_measurement = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('high risk', 'High Risk'), ('intermediate risk', 'Intermediate Risk'), ('low risk', 'Low Risk'),])
    ace_flag = models.CharField(max_length=10, blank=True, null=True, choices=[
        ('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    assist = models.OneToOneField(
        MeasurementAssist, on_delete=models.CASCADE, null=True, blank=True)
    overall_flag = models.CharField(max_length=10, blank=True, null=True, choices=[
        ('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')])
    created_at = models.DateTimeField(
        default=timezone.now)

    def __str__(self):
        return f'Measurement for {self.user.username}'
