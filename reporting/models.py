from django.db import models
from django.utils import timezone
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



class UserArchive(models.Model):
    # Personal Information
    identity_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    is_gyalsung = models.BooleanField(default=False)
    academy_code = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=20, null=True)

    # User Agency Details
    user_code = models.CharField(max_length=100, blank=True, null=True)
    parent_status = models.CharField(max_length=100, blank=True, null=True)
    current_living_with = models.CharField(max_length=100, blank=True, null=True)
    user_role_agency = models.CharField(max_length=100, blank=True, null=True)
    user_class = models.CharField(max_length=100, blank=True, null=True)
    user_stream = models.CharField(max_length=100, blank=True, null=True)
    user_sub_class = models.CharField(max_length=100, blank=True, null=True)

    # Location Details
    agency_code = models.CharField(max_length=100, blank=True, null=True)
    agency_name = models.CharField(max_length=100, blank=True, null=True)
    agency_parent = models.CharField(max_length=100, null=True, blank=True)
    present_dzongkhag = models.CharField(max_length=100, null=True, blank=True)
    present_gewog = models.CharField(max_length=100, null=True, blank=True)
    present_village = models.CharField(max_length=100, null=True, blank=True)
    ps_add_village = models.CharField(max_length=100, blank=True, null=True)
    ps_add_gewog = models.CharField(max_length=100, blank=True, null=True)
    ps_add_dzongkhag = models.CharField(max_length=100, blank=True, null=True)

    # Substance Use Information
    gad_measurement = models.CharField(max_length=50, blank=True, null=True)
    gad_flag = models.CharField(max_length=10, blank=True, null=True)
    phq_measurement = models.CharField(max_length=50, blank=True, null=True)
    phq_flag = models.CharField(max_length=10, blank=True, null=True)
    suicidal_measurement = models.CharField(max_length=50, blank=True, null=True)
    suicidal_flag = models.CharField(max_length=10, blank=True, null=True)
    ace_measurement = models.CharField(max_length=50, blank=True, null=True)
    ace_flag = models.CharField(max_length=10, blank=True, null=True)
    overall_flag = models.CharField(max_length=10, blank=True, null=True)
    alcoholic_measurement = models.CharField(max_length=50, blank=True, null=True)
    alcoholic_flag = models.CharField(max_length=50, blank=True, null=True)
    tobacco_measurement = models.CharField(max_length=50, blank=True, null=True)
    tobacco_flag = models.CharField(max_length=50, blank=True, null=True)
    cannabis_measurement = models.CharField(max_length=50, blank=True, null=True)
    cannabis_flag = models.CharField(max_length=50, blank=True, null=True)
    cocaine_measurement = models.CharField(max_length=50, blank=True, null=True)
    cocaine_flag = models.CharField(max_length=50, blank=True, null=True)
    amphetamine_measurement = models.CharField(max_length=50, blank=True, null=True)
    amphetamine_flag = models.CharField(max_length=50, blank=True, null=True)
    inhalants_measurement = models.CharField(max_length=50, blank=True, null=True)
    inhalants_flag = models.CharField(max_length=50, blank=True, null=True)
    sedatives_measurement = models.CharField(max_length=50, blank=True, null=True)
    sedatives_flag = models.CharField(max_length=50, blank=True, null=True)
    hallucinogens_measurement = models.CharField(max_length=50, blank=True, null=True)
    hallucinogens_flag = models.CharField(max_length=50, blank=True, null=True)
    opioids_measurement = models.CharField(max_length=50, blank=True, null=True)
    opioids_flag = models.CharField(max_length=50, blank=True, null=True)
    injection_measurement = models.CharField(max_length=50, blank=True, null=True)
    injection_flag = models.CharField(max_length=50, blank=True, null=True)
    other_measurement = models.CharField(max_length=50, blank=True, null=True)
    other_flag = models.CharField(max_length=50, blank=True, null=True)
    other_name = models.CharField(max_length=100, blank=True, null=True)

    # Submission Details
    test_type = models.CharField(max_length=100, blank=True, null=True)
    rescreened = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    # Screening and Assessment
    assessment_status = models.CharField(max_length=20, default='Not Conducted', blank=True, null=True)
    case_status = models.CharField(max_length=20, default='On Going', blank=True, null=True)
    counseling = models.CharField(max_length=20, default='Waiting List', blank=True, null=True)
    follow_up = models.CharField(max_length=255, blank=True)
    comments = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now)
    referred = models.CharField(max_length=20, default='Not Referred')

    # Rescreening Details
    gad_rescreening_interpretation = models.CharField(max_length=50, blank=True, null=True)
    gad_rescreening_score = models.CharField(max_length=10, blank=True, null=True)
    phq_rescreening_interpretation = models.CharField(max_length=50, blank=True, null=True)
    phq_rescreening_score = models.CharField(max_length=10, blank=True, null=True)
    suicidal_rescreening_interpretation = models.CharField(max_length=50, blank=True, null=True)
    suicidal_rescreening_score = models.CharField(max_length=10, blank=True, null=True)
    ace_rescreening_interpretation = models.CharField(max_length=50, blank=True, null=True)
    ace_rescreening_score = models.CharField(max_length=10, blank=True, null=True)

    alcoholic_rescreening_interpretation = models.CharField(max_length=50, blank=True, null=True)
    alcoholic_rescreening_score = models.CharField(max_length=50, blank=True, null=True)
    tobacco_rescreening_interpretation = models.CharField(max_length=50, blank=True, null=True)
    tobacco_rescreening_score = models.CharField(max_length=50, blank=True, null=True)
    cannabis_rescreening_interpretation = models.CharField(max_length=50, blank=True, null=True)
    cannabis_rescreening_score = models.CharField(max_length=50, blank=True, null=True)
    cocaine_rescreening_interpretation = models.CharField(max_length=50, blank=True, null=True)
    cocaine_rescreening_score = models.CharField(max_length=50, blank=True, null=True)
    amphetamine_rescreening_interpretation = models.CharField(max_length=50, blank=True, null=True)
    amphetamine_rescreening_score = models.CharField(max_length=50, blank=True, null=True)
    inhalants_rescreening_interpretation = models.CharField(max_length=50, blank=True, null=True)
    inhalants_rescreening_score = models.CharField(max_length=50, blank=True, null=True)
    sedatives_rescreening_interpretation = models.CharField(max_length=50, blank=True, null=True)
    sedatives_rescreening_score = models.CharField(max_length=50, blank=True, null=True)
    hallucinogens_rescreening_interpretation = models.CharField(max_length=50, blank=True, null=True)
    hallucinogens_rescreening_score = models.CharField(max_length=50, blank=True, null=True)
    opioids_rescreening_interpretation = models.CharField(max_length=50, blank=True, null=True)
    opioids_rescreening_score = models.CharField(max_length=50, blank=True, null=True)
    injection_rescreening_interpretation = models.CharField(max_length=50, blank=True, null=True)
    injection_rescreening_score = models.CharField(max_length=50, blank=True, null=True)
    other_rescreening_interpretation = models.CharField(max_length=50, blank=True, null=True)
    other_rescreening_score = models.CharField(max_length=50, blank=True, null=True)
    other_rescreening_name = models.CharField(max_length=100, blank=True, null=True)

    # Referral Details
    referred_by = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    referred_to = models.CharField(max_length=100, null=True, blank=True)
    referred_to_name = models.CharField(max_length=100, null=True, blank=True)
    referral_status = models.CharField(max_length=20, default='Awaiting')
    referral_remarks = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "User Archive"
        verbose_name_plural = "User Archives"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.identity_number}"