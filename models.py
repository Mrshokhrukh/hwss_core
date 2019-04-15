# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccessAgency(models.Model):
    agency_code = models.CharField(unique=True, max_length=100)
    agency_name = models.CharField(max_length=100)
    agency_parent = models.CharField(max_length=100, blank=True, null=True)
    present_dzongkhag = models.CharField(max_length=100, blank=True, null=True)
    present_gewog = models.CharField(max_length=100, blank=True, null=True)
    present_village = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'access_agency'


class AccessCustomuser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=50, blank=True, null=True)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    identity_number = models.CharField(unique=True, max_length=50)
    nationality = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    email = models.CharField(unique=True, max_length=254, blank=True, null=True)
    mob_number = models.CharField(max_length=15, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    perm_add_village = models.CharField(max_length=100)
    perm_add_gewog = models.CharField(max_length=100)
    perm_add_dzongkhag = models.CharField(max_length=100)
    profile_picture = models.CharField(max_length=100, blank=True, null=True)
    ps_add_village = models.CharField(max_length=100, blank=True, null=True)
    ps_add_gewog = models.CharField(max_length=100, blank=True, null=True)
    ps_add_dzongkhag = models.CharField(max_length=100, blank=True, null=True)
    is_gyalsung = models.IntegerField()
    academy_code = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateTimeField()
    role = models.CharField(max_length=20, blank=True, null=True)
    access_level = models.IntegerField()
    active_agency = models.ForeignKey(AccessAgency, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'access_customuser'


class AccessCustomuserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(AccessCustomuser, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'access_customuser_groups'
        unique_together = (('customuser', 'group'),)


class AccessCustomuserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(AccessCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'access_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)


class AccessPrerecordeduser(models.Model):
    username = models.CharField(unique=True, max_length=150)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    identity_number = models.CharField(unique=True, max_length=50)
    nationality = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    email = models.CharField(unique=True, max_length=254)
    mob_number = models.CharField(max_length=15)
    father_name = models.CharField(max_length=50, blank=True, null=True)
    mother_name = models.CharField(max_length=50, blank=True, null=True)
    perm_add_village = models.CharField(max_length=100)
    perm_add_gewog = models.CharField(max_length=100)
    perm_add_dzongkhag = models.CharField(max_length=100)
    profile_picture = models.CharField(max_length=100, blank=True, null=True)
    is_gyalsung = models.IntegerField()
    academy_code = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateTimeField()
    role = models.CharField(max_length=100, blank=True, null=True)
    access_level = models.CharField(max_length=100, blank=True, null=True)
    is_registered = models.IntegerField()
    agency_name = models.CharField(max_length=100, blank=True, null=True)
    agency_code = models.CharField(max_length=100, blank=True, null=True)
    user_code = models.CharField(max_length=100, blank=True, null=True)
    ps_add_village = models.CharField(max_length=100, blank=True, null=True)
    ps_add_gewog = models.CharField(max_length=100, blank=True, null=True)
    ps_add_dzongkhag = models.CharField(max_length=100, blank=True, null=True)
    parent_occupation = models.CharField(max_length=100, blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_occupation = models.CharField(max_length=100, blank=True, null=True)
    parent_status = models.CharField(max_length=100, blank=True, null=True)
    current_living_with = models.CharField(max_length=100, blank=True, null=True)
    user_role_agency = models.CharField(max_length=100, blank=True, null=True)
    user_class = models.CharField(max_length=100, blank=True, null=True)
    user_sub_class = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'access_prerecordeduser'


class AccessUseragency(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_code = models.CharField(max_length=100)
    parent_occupation = models.CharField(max_length=100, blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_occupation = models.CharField(max_length=100, blank=True, null=True)
    parent_status = models.CharField(max_length=100, blank=True, null=True)
    current_living_with = models.CharField(max_length=100, blank=True, null=True)
    user_role_agency = models.CharField(max_length=100)
    user_class = models.CharField(max_length=100, blank=True, null=True)
    user_stream = models.CharField(max_length=100, blank=True, null=True)
    user_sub_class = models.CharField(max_length=100, blank=True, null=True)
    agency = models.ForeignKey(AccessAgency, models.DO_NOTHING)
    user = models.OneToOneField(AccessCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'access_useragency'


class AdminInterfaceTheme(models.Model):
    name = models.CharField(unique=True, max_length=50)
    active = models.IntegerField()
    title = models.CharField(max_length=50)
    title_visible = models.IntegerField()
    logo = models.CharField(max_length=100)
    logo_visible = models.IntegerField()
    css_header_background_color = models.CharField(max_length=10)
    title_color = models.CharField(max_length=10)
    css_header_text_color = models.CharField(max_length=10)
    css_header_link_color = models.CharField(max_length=10)
    css_header_link_hover_color = models.CharField(max_length=10)
    css_module_background_color = models.CharField(max_length=10)
    css_module_text_color = models.CharField(max_length=10)
    css_module_link_color = models.CharField(max_length=10)
    css_module_link_hover_color = models.CharField(max_length=10)
    css_module_rounded_corners = models.IntegerField()
    css_generic_link_color = models.CharField(max_length=10)
    css_generic_link_hover_color = models.CharField(max_length=10)
    css_save_button_background_color = models.CharField(max_length=10)
    css_save_button_background_hover_color = models.CharField(max_length=10)
    css_save_button_text_color = models.CharField(max_length=10)
    css_delete_button_background_color = models.CharField(max_length=10)
    css_delete_button_background_hover_color = models.CharField(max_length=10)
    css_delete_button_text_color = models.CharField(max_length=10)
    list_filter_dropdown = models.IntegerField()
    related_modal_active = models.IntegerField()
    related_modal_background_color = models.CharField(max_length=10)
    related_modal_rounded_corners = models.IntegerField()
    logo_color = models.CharField(max_length=10)
    recent_actions_visible = models.IntegerField()
    favicon = models.CharField(max_length=100)
    related_modal_background_opacity = models.CharField(max_length=5)
    env_name = models.CharField(max_length=50)
    env_visible_in_header = models.IntegerField()
    env_color = models.CharField(max_length=10)
    env_visible_in_favicon = models.IntegerField()
    related_modal_close_button_visible = models.IntegerField()
    language_chooser_active = models.IntegerField()
    language_chooser_display = models.CharField(max_length=10)
    list_filter_sticky = models.IntegerField()
    form_pagination_sticky = models.IntegerField()
    form_submit_sticky = models.IntegerField()
    css_module_background_selected_color = models.CharField(max_length=10)
    css_module_link_selected_color = models.CharField(max_length=10)
    logo_max_height = models.PositiveSmallIntegerField()
    logo_max_width = models.PositiveSmallIntegerField()
    foldable_apps = models.IntegerField()
    language_chooser_control = models.CharField(max_length=20)
    list_filter_highlight = models.IntegerField()
    list_filter_removal_links = models.IntegerField()
    show_fieldsets_as_tabs = models.IntegerField()
    show_inlines_as_tabs = models.IntegerField()
    css_generic_link_active_color = models.CharField(max_length=10)
    collapsible_stacked_inlines = models.IntegerField()
    collapsible_stacked_inlines_collapsed = models.IntegerField()
    collapsible_tabular_inlines = models.IntegerField()
    collapsible_tabular_inlines_collapsed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'admin_interface_theme'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AccessCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccessCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class MeasurementActiveuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(AccessCustomuser, models.DO_NOTHING)
    user_submission = models.ForeignKey('MeasurementUsersubmission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'measurement_activeuser'


class MeasurementActiveuserSubstancesUsed(models.Model):
    id = models.BigAutoField(primary_key=True)
    activeuser = models.ForeignKey(MeasurementActiveuser, models.DO_NOTHING)
    measurementsubstance = models.ForeignKey('MeasurementMeasurementsubstance', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'measurement_activeuser_substances_used'
        unique_together = (('activeuser', 'measurementsubstance'),)


class MeasurementLifetimeuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(AccessCustomuser, models.DO_NOTHING)
    user_submission = models.ForeignKey('MeasurementUsersubmission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'measurement_lifetimeuser'


class MeasurementLifetimeuserSubstancesUsed(models.Model):
    id = models.BigAutoField(primary_key=True)
    lifetimeuser = models.ForeignKey(MeasurementLifetimeuser, models.DO_NOTHING)
    measurementsubstance = models.ForeignKey('MeasurementMeasurementsubstance', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'measurement_lifetimeuser_substances_used'
        unique_together = (('lifetimeuser', 'measurementsubstance'),)


class MeasurementMeasurement(models.Model):
    id = models.BigAutoField(primary_key=True)
    gad_measurement = models.CharField(max_length=50, blank=True, null=True)
    gad_flag = models.CharField(max_length=10, blank=True, null=True)
    phq_measurement = models.CharField(max_length=50, blank=True, null=True)
    phq_flag = models.CharField(max_length=10, blank=True, null=True)
    suicidal_measurement = models.CharField(max_length=50, blank=True, null=True)
    suicidal_flag = models.CharField(max_length=10, blank=True, null=True)
    ace_measurement = models.CharField(max_length=50, blank=True, null=True)
    ace_flag = models.CharField(max_length=10, blank=True, null=True)
    overall_flag = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField()
    user = models.OneToOneField(AccessCustomuser, models.DO_NOTHING)
    assist = models.OneToOneField('MeasurementMeasurementassist', models.DO_NOTHING, blank=True, null=True)
    user_submission = models.ForeignKey('MeasurementUsersubmission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'measurement_measurement'


class MeasurementMeasurementassist(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    created_at = models.DateTimeField()
    user = models.OneToOneField(AccessCustomuser, models.DO_NOTHING)
    user_submission = models.ForeignKey('MeasurementUsersubmission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'measurement_measurementassist'


class MeasurementMeasurementsubstance(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'measurement_measurementsubstance'


class MeasurementQuestionset(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    test_type = models.ForeignKey('MeasurementTesttype', models.DO_NOTHING)
    user_submission = models.ForeignKey('MeasurementUsersubmission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'measurement_questionset'


class MeasurementSubmission(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    score = models.IntegerField(blank=True, null=True)
    substance = models.CharField(max_length=100)
    specify = models.CharField(max_length=100)
    diagnosis = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    question_set = models.ForeignKey(MeasurementQuestionset, models.DO_NOTHING)
    user_submission = models.ForeignKey('MeasurementUsersubmission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'measurement_submission'


class MeasurementTesttype(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'measurement_testtype'


class MeasurementUsersubmission(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    test_type = models.ForeignKey(MeasurementTesttype, models.DO_NOTHING)
    user = models.ForeignKey(AccessCustomuser, models.DO_NOTHING)
    rescreened = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'measurement_usersubmission'


class MonitoringReferral(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    referred_to_name = models.CharField(max_length=100, blank=True, null=True)
    referral_status = models.CharField(max_length=20)
    referral_remarks = models.TextField(blank=True, null=True)
    referred_by = models.ForeignKey(AccessCustomuser, models.DO_NOTHING, blank=True, null=True)
    referred_to = models.ForeignKey(AccessCustomuser, models.DO_NOTHING, related_name='monitoringreferral_referred_to_set', blank=True, null=True)
    user = models.ForeignKey(AccessCustomuser, models.DO_NOTHING, related_name='monitoringreferral_user_set')
    service_and_treatment_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monitoring_referral'


class MonitoringRescreening(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AccessCustomuser, models.DO_NOTHING)
    service_and_treatment = models.ForeignKey('MonitoringServiceandtreatment', models.DO_NOTHING, blank=True, null=True)
    rescreening_count = models.IntegerField()
    ace_data = models.JSONField(blank=True, null=True)
    gad_data = models.JSONField(blank=True, null=True)
    phq_data = models.JSONField(blank=True, null=True)
    referral = models.ForeignKey(MonitoringReferral, models.DO_NOTHING, blank=True, null=True)
    rescreened = models.IntegerField()
    school_env_data = models.JSONField(blank=True, null=True)
    submission_date = models.DateTimeField()
    ace_interpretation = models.CharField(max_length=255, blank=True, null=True)
    ace_score = models.IntegerField(blank=True, null=True)
    gad_interpretation = models.CharField(max_length=255, blank=True, null=True)
    gad_score = models.IntegerField(blank=True, null=True)
    phq_interpretation = models.CharField(max_length=255, blank=True, null=True)
    phq_score = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monitoring_rescreening'


class MonitoringServiceandtreatment(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    assessment_status = models.CharField(max_length=20)
    case_status = models.CharField(max_length=20)
    counseling = models.CharField(max_length=20)
    follow_up = models.CharField(max_length=255)
    comments = models.TextField(blank=True, null=True)
    user = models.ForeignKey(AccessCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'monitoring_serviceandtreatment'


class MonitoringSubstance(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'monitoring_substance'


class MonitoringSubstanceriskmeasurement(models.Model):
    id = models.BigAutoField(primary_key=True)
    measurement = models.FloatField()
    risk_flag = models.CharField(max_length=250)
    rescreening = models.ForeignKey(MonitoringRescreening, models.DO_NOTHING)
    substance = models.ForeignKey(MonitoringSubstance, models.DO_NOTHING)
    total_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monitoring_substanceriskmeasurement'


class ReportingReporting(models.Model):
    id = models.BigAutoField(primary_key=True)
    agency_code = models.CharField(max_length=100, blank=True, null=True)
    agency_name = models.CharField(max_length=100, blank=True, null=True)
    present_dzongkhag = models.CharField(max_length=100, blank=True, null=True)
    present_gewog = models.CharField(max_length=100, blank=True, null=True)
    present_village = models.CharField(max_length=100, blank=True, null=True)
    user_code = models.CharField(max_length=100, blank=True, null=True)
    parent_occupation = models.CharField(max_length=100, blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_occupation = models.CharField(max_length=100, blank=True, null=True)
    parent_status = models.CharField(max_length=100, blank=True, null=True)
    current_living_with = models.CharField(max_length=100, blank=True, null=True)
    user_role_agency = models.CharField(max_length=100, blank=True, null=True)
    user_class = models.CharField(max_length=100, blank=True, null=True)
    user_stream = models.CharField(max_length=100, blank=True, null=True)
    user_sub_class = models.CharField(max_length=100, blank=True, null=True)
    gad_measurement = models.CharField(max_length=50, blank=True, null=True)
    phq_measurement = models.CharField(max_length=50, blank=True, null=True)
    suicidal_measurement = models.CharField(max_length=50, blank=True, null=True)
    ace_measurement = models.CharField(max_length=50, blank=True, null=True)
    overall_flag = models.CharField(max_length=10, blank=True, null=True)
    assessment_status = models.CharField(max_length=20, blank=True, null=True)
    case_status = models.CharField(max_length=20, blank=True, null=True)
    counseling = models.CharField(max_length=20, blank=True, null=True)
    follow_up = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    referral_status = models.CharField(max_length=20, blank=True, null=True)
    referral_remarks = models.TextField(blank=True, null=True)
    rescreening_count = models.PositiveIntegerField()
    user = models.ForeignKey(AccessCustomuser, models.DO_NOTHING)
    alcoholic_flag = models.CharField(max_length=50, blank=True, null=True)
    alcoholic_measurement = models.CharField(max_length=50, blank=True, null=True)
    amphetamine_flag = models.CharField(max_length=50, blank=True, null=True)
    amphetamine_measurement = models.CharField(max_length=50, blank=True, null=True)
    cannabis_flag = models.CharField(max_length=50, blank=True, null=True)
    cannabis_measurement = models.CharField(max_length=50, blank=True, null=True)
    cocaine_flag = models.CharField(max_length=50, blank=True, null=True)
    cocaine_measurement = models.CharField(max_length=50, blank=True, null=True)
    hallucinogens_flag = models.CharField(max_length=50, blank=True, null=True)
    hallucinogens_measurement = models.CharField(max_length=50, blank=True, null=True)
    inhalants_flag = models.CharField(max_length=50, blank=True, null=True)
    inhalants_measurement = models.CharField(max_length=50, blank=True, null=True)
    injection_flag = models.CharField(max_length=50, blank=True, null=True)
    injection_measurement = models.CharField(max_length=50, blank=True, null=True)
    opioids_flag = models.CharField(max_length=50, blank=True, null=True)
    opioids_measurement = models.CharField(max_length=50, blank=True, null=True)
    other_flag = models.CharField(max_length=50, blank=True, null=True)
    other_measurement = models.CharField(max_length=50, blank=True, null=True)
    other_name = models.CharField(max_length=100, blank=True, null=True)
    sedatives_flag = models.CharField(max_length=50, blank=True, null=True)
    sedatives_measurement = models.CharField(max_length=50, blank=True, null=True)
    tobacco_flag = models.CharField(max_length=50, blank=True, null=True)
    tobacco_measurement = models.CharField(max_length=50, blank=True, null=True)
    past_diagnosis = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reporting_reporting'


class ScreeningCase(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'screening_case'


class ScreeningCasebasedsubmission(models.Model):
    id = models.BigAutoField(primary_key=True)
    gad_data = models.JSONField(blank=True, null=True)
    gad_score = models.IntegerField(blank=True, null=True)
    gad_interpretation = models.CharField(max_length=255, blank=True, null=True)
    phq_data = models.JSONField(blank=True, null=True)
    phq_score = models.IntegerField(blank=True, null=True)
    phq_interpretation = models.CharField(max_length=255, blank=True, null=True)
    ace_data = models.JSONField(blank=True, null=True)
    ace_score = models.IntegerField(blank=True, null=True)
    ace_interpretation = models.CharField(max_length=255, blank=True, null=True)
    school_env_data = models.JSONField(blank=True, null=True)
    submission_date = models.DateTimeField()
    case = models.ForeignKey(ScreeningCase, models.DO_NOTHING)
    referral = models.ForeignKey(MonitoringReferral, models.DO_NOTHING, blank=True, null=True)
    service_and_treatment = models.ForeignKey(MonitoringServiceandtreatment, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'screening_casebasedsubmission'


class ScreeningCasescreening(models.Model):
    id = models.BigAutoField(primary_key=True)
    case_name = models.CharField(max_length=255)
    purpose = models.CharField(max_length=20)
    dzongkhag = models.CharField(max_length=50)
    date = models.DateField()
    counselor = models.CharField(max_length=255)
    registration_lockout_end_time = models.DateTimeField(blank=True, null=True)
    submission = models.ForeignKey(MeasurementUsersubmission, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccessCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'screening_casescreening'


class ScreeningCasesubstance(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'screening_casesubstance'


class ScreeningCasesubstanceriskmeasurement(models.Model):
    id = models.BigAutoField(primary_key=True)
    measurement = models.FloatField()
    risk_flag = models.CharField(max_length=250)
    total_score = models.FloatField(blank=True, null=True)
    case_submission = models.ForeignKey(ScreeningCasebasedsubmission, models.DO_NOTHING)
    substance = models.ForeignKey(ScreeningCasesubstance, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'screening_casesubstanceriskmeasurement'


class ScreeningEvent(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'screening_event'


class ScreeningEventbasedsubmission(models.Model):
    id = models.BigAutoField(primary_key=True)
    gad_data = models.JSONField(blank=True, null=True)
    gad_score = models.IntegerField(blank=True, null=True)
    gad_interpretation = models.CharField(max_length=255, blank=True, null=True)
    phq_data = models.JSONField(blank=True, null=True)
    phq_score = models.IntegerField(blank=True, null=True)
    phq_interpretation = models.CharField(max_length=255, blank=True, null=True)
    ace_data = models.JSONField(blank=True, null=True)
    ace_score = models.IntegerField(blank=True, null=True)
    ace_interpretation = models.CharField(max_length=255, blank=True, null=True)
    school_env_data = models.JSONField(blank=True, null=True)
    submission_date = models.DateTimeField()
    event = models.ForeignKey(ScreeningEvent, models.DO_NOTHING)
    referral = models.ForeignKey(MonitoringReferral, models.DO_NOTHING, blank=True, null=True)
    service_and_treatment = models.ForeignKey(MonitoringServiceandtreatment, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'screening_eventbasedsubmission'


class ScreeningEventscreening(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_name = models.CharField(max_length=255)
    event_purpose = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.IntegerField()
    counselor = models.CharField(max_length=255)
    approval_status = models.CharField(max_length=20)
    remarks = models.TextField(blank=True, null=True)
    registration_lockout_end_time = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'screening_eventscreening'


class ScreeningEventsubstance(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'screening_eventsubstance'


class ScreeningEventsubstanceriskmeasurement(models.Model):
    id = models.BigAutoField(primary_key=True)
    measurement = models.FloatField()
    risk_flag = models.CharField(max_length=250)
    total_score = models.FloatField(blank=True, null=True)
    event_submission = models.ForeignKey(ScreeningEventbasedsubmission, models.DO_NOTHING)
    substance = models.ForeignKey(ScreeningEventsubstance, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'screening_eventsubstanceriskmeasurement'


class ScreeningScreeneduser(models.Model):
    id = models.BigAutoField(primary_key=True)
    screening_date = models.DateField()
    event_screening = models.ForeignKey(ScreeningEventscreening, models.DO_NOTHING)
    user = models.ForeignKey(AccessCustomuser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'screening_screeneduser'


class SettingsModuleAppconfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    login_logo = models.CharField(max_length=100)
    registration_logo = models.CharField(max_length=100)
    landing_page_logo = models.CharField(max_length=100, blank=True, null=True)
    landing_img_bg = models.CharField(max_length=100, blank=True, null=True)
    landing_tag_line = models.CharField(max_length=255, blank=True, null=True)
    dashboard_logo = models.CharField(max_length=100)
    carousel_image_1 = models.CharField(max_length=100, blank=True, null=True)
    carousel_image_2 = models.CharField(max_length=100, blank=True, null=True)
    carousel_image_3 = models.CharField(max_length=100, blank=True, null=True)
    carousel_image_4 = models.CharField(max_length=100, blank=True, null=True)
    app_name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=255)
    helpline_number_1 = models.CharField(max_length=50)
    helpline_number_2 = models.CharField(max_length=50)
    response_service_logo = models.CharField(max_length=100)
    cluster_test_title = models.CharField(max_length=50, blank=True, null=True)
    cluster_test_content = models.TextField(blank=True, null=True)
    cluster_test_disclaimer = models.TextField(blank=True, null=True)
    cluster_test_icon = models.CharField(max_length=100, blank=True, null=True)
    copyright_message = models.CharField(max_length=255, blank=True, null=True)
    google_play_link = models.CharField(max_length=255, blank=True, null=True)
    apple_appstore_link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'settings_module_appconfig'


class SettingsModuleMenuitem(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    route = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'settings_module_menuitem'


class SettingsModuleMenuitemRoles(models.Model):
    id = models.BigAutoField(primary_key=True)
    menuitem = models.ForeignKey(SettingsModuleMenuitem, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'settings_module_menuitem_roles'
        unique_together = (('menuitem', 'group'),)


class SettingsModuleNotification(models.Model):
    id = models.BigAutoField(primary_key=True)
    message = models.TextField()
    timestamp = models.DateTimeField()
    is_read = models.IntegerField()
    recipient = models.ForeignKey(AccessCustomuser, models.DO_NOTHING)
    sender = models.ForeignKey(AccessCustomuser, models.DO_NOTHING, related_name='settingsmodulenotification_sender_set')

    class Meta:
        managed = False
        db_table = 'settings_module_notification'


class SettingsModuleVideo(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    thumbnail = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    description = models.TextField()
    video_link = models.CharField(max_length=200)
    video_file = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'settings_module_video'
