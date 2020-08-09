from django.db import models


class GyalsungUserProfile(models.Model):
    GENDER_CHOICES = [("M", "Male"), ("F", "Female"), ("O", "Other")]

    SEVERITY_CHOICES = [
        ("severe", "Severe"),
        ("moderately_severe", "Moderately Severe"),
        ("moderate", "Moderate"),
        ("mild", "Mild"),
        ("minimal", "Minimal"),
    ]

    username = models.CharField(max_length=150)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField()
    identity_number = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    ps_add_village = models.CharField(max_length=255, null=True, blank=True)
    ps_add_gewog = models.CharField(max_length=255, null=True, blank=True)
    ps_add_dzongkhag = models.CharField(max_length=255, null=True, blank=True)
    academy_code = models.CharField(max_length=20, null=True, blank=True)
    batch_number = models.CharField(max_length=20, null=True, blank=True)
    prev_school = models.CharField(max_length=255, null=True, blank=True)
    phq9_score = models.IntegerField(null=True, blank=True)
    phq9_flag = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True
    )
    suicidal_score = models.IntegerField(null=True, blank=True)
    suicidal_flag = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True
    )
    gad7_score = models.IntegerField(null=True, blank=True)
    gad7_flag = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True
    )
    tobacco_score = models.IntegerField(null=True, blank=True)
    tobacco_flag = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True
    )
    alcohol_score = models.IntegerField(null=True, blank=True)
    alcohol_flag = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True
    )
    cannabis_score = models.IntegerField(null=True, blank=True)
    cannabis_flag = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True
    )
    cocaine_score = models.IntegerField(null=True, blank=True)
    cocaine_flag = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True
    )
    amphetamine_score = models.IntegerField(null=True, blank=True)
    amphetamine_flag = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True
    )
    inhalants_score = models.IntegerField(null=True, blank=True)
    inhalants_flag = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True
    )
    sedatives_score = models.IntegerField(null=True, blank=True)
    sedatives_flag = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True
    )
    hallucinogens_score = models.IntegerField(null=True, blank=True)
    hallucinogens_flag = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True
    )
    opioids_score = models.IntegerField(null=True, blank=True)
    opioids_flag = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True
    )
    other_score = models.IntegerField(null=True, blank=True)
    other_flag = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True
    )
    other_name = models.CharField(max_length=255, blank=True, null=True)
    injection_use_score = models.IntegerField(null=True, blank=True)
    injection_use_flag = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True
    )

    def __str__(self):
        return self.username
