from django.db import models
from access.models import CustomUser

User = CustomUser

class Reporting(models.Model):
    # User details from the access module
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agency_code = models.CharField(max_length=100, blank=True, null=True, help_text="Agency code associated with the user")
    agency_name = models.CharField(max_length=100, blank=True, null=True, help_text="Agency name associated with the user")
    present_dzongkhag = models.CharField(max_length=100, blank=True, null=True, help_text="Present dzongkhag of the user")
    present_gewog = models.CharField(max_length=100, blank=True, null=True, help_text="Present gewog of the user")
    present_village = models.CharField(max_length=100, blank=True, null=True, help_text="Present village of the user")
    user_code = models.CharField(max_length=100, blank=True, null=True, help_text="Code assigned to the user within the agency")
    parent_occupation = models.CharField(max_length=100, blank=True, null=True, help_text="Occupation of the user's parent")
    guardian_name = models.CharField(max_length=100, blank=True, null=True, help_text="Name of the user's guardian")
    guardian_occupation = models.CharField(max_length=100, blank=True, null=True, help_text="Occupation of the user's guardian")
    parent_status = models.CharField(max_length=100, blank=True, null=True, help_text="Status of the user's parent")
    current_living_with = models.CharField(max_length=100, blank=True, null=True, help_text="Who the user is currently living with")
    user_role_agency = models.CharField(max_length=100, blank=True, null=True, help_text="Role of the user within the agency")
    user_class = models.CharField(max_length=100, blank=True, null=True, help_text="Class of the user")
    user_stream = models.CharField(max_length=100, blank=True, null=True, help_text="Stream of the user")
    user_sub_class = models.CharField(max_length=100, blank=True, null=True, help_text="Subclass of the user")

    # Measurement data
    past_diagnosis = models.CharField(max_length=50, blank=True, null=True, help_text="Past Diagnosis")
    gad_measurement = models.CharField(max_length=50, blank=True, null=True, help_text="GAD measurement")
    phq_measurement = models.CharField(max_length=50, blank=True, null=True, help_text="PHQ measurement")
    suicidal_measurement = models.CharField(max_length=50, blank=True, null=True, help_text="Suicidal measurement")
    ace_measurement = models.CharField(max_length=50, blank=True, null=True, help_text="ACE measurement")
    overall_flag = models.CharField(max_length=10, blank=True, null=True, help_text="Overall flag")

    # MeasurementAssist data
    alcoholic_measurement = models.CharField(max_length=50, blank=True, null=True, help_text="Alcoholic measurement")
    alcoholic_flag = models.CharField(max_length=50, blank=True, null=True, help_text="Alcoholic flag")
    tobacco_measurement = models.CharField(max_length=50, blank=True, null=True, help_text="Tobacco measurement")
    tobacco_flag = models.CharField(max_length=50, blank=True, null=True, help_text="Tobacco flag")
    cannabis_measurement = models.CharField(max_length=50, blank=True, null=True, help_text="Cannabis measurement")
    cannabis_flag = models.CharField(max_length=50, blank=True, null=True, help_text="Cannabis flag")
    cocaine_measurement = models.CharField(max_length=50, blank=True, null=True, help_text="Cocaine measurement")
    cocaine_flag = models.CharField(max_length=50, blank=True, null=True, help_text="Cocaine flag")
    amphetamine_measurement = models.CharField(max_length=50, blank=True, null=True, help_text="Amphetamine measurement")
    amphetamine_flag = models.CharField(max_length=50, blank=True, null=True, help_text="Amphetamine flag")
    inhalants_measurement = models.CharField(max_length=50, blank=True, null=True, help_text="Inhalants measurement")
    inhalants_flag = models.CharField(max_length=50, blank=True, null=True, help_text="Inhalants flag")
    sedatives_measurement = models.CharField(max_length=50, blank=True, null=True, help_text="Sedatives measurement")
    sedatives_flag = models.CharField(max_length=50, blank=True, null=True, help_text="Sedatives flag")
    hallucinogens_measurement = models.CharField(max_length=50, blank=True, null=True, help_text="Hallucinogens measurement")
    hallucinogens_flag = models.CharField(max_length=50, blank=True, null=True, help_text="Hallucinogens flag")
    opioids_measurement = models.CharField(max_length=50, blank=True, null=True, help_text="Opioids measurement")
    opioids_flag = models.CharField(max_length=50, blank=True, null=True, help_text="Opioids flag")
    injection_measurement = models.CharField(max_length=50, blank=True, null=True, help_text="Injection measurement")
    injection_flag = models.CharField(max_length=50, blank=True, null=True, help_text="Injection flag")
    other_measurement = models.CharField(max_length=50, blank=True, null=True, help_text="Other substance measurement")
    other_flag = models.CharField(max_length=50, blank=True, null=True, help_text="Other substance flag")
    other_name = models.CharField(max_length=100, blank=True, null=True, help_text="Name of other substance")
    
    # Monitoring data
    assessment_status = models.CharField(max_length=20, blank=True, null=True, help_text="Assessment status")
    case_status = models.CharField(max_length=20, blank=True, null=True, help_text="Case status")
    counseling = models.CharField(max_length=20, blank=True, null=True, help_text="Counseling status")
    follow_up = models.CharField(max_length=255, blank=True, null=True, help_text="Follow-up details")
    comments = models.TextField(blank=True, null=True, help_text="Additional comments")
    referral_status = models.CharField(max_length=20, blank=True, null=True, help_text="Referral status")
    referral_remarks = models.TextField(blank=True, null=True, help_text="Remarks related to referral")
    rescreening_count = models.PositiveIntegerField(default=0, help_text="Number of rescreenings conducted")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporting for {self.user.username}"
