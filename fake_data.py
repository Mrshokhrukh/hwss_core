import os
import django
from django.conf import settings
from faker import Faker

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hwss_core.settings')
django.setup()

# Create an instance of Faker
fake = Faker()

from access.models import Agency, UserAgency, CustomUser
from measurement.models import Submission, MeasurementAssist, Measurement, UserSubmission, QuestionSet, TestType

# Generate fake data for TestType model
test_types = ['Cluster Screening']  # Adjust as needed
for test_type_name in test_types:
    TestType.objects.create(name=test_type_name)

# Generate fake data for UserSubmission and QuestionSet models
for _ in range(10):
    user = CustomUser.objects.order_by('?').first()
    test_type = TestType.objects.order_by('?').first()
    user_submission = UserSubmission.objects.create(
        user=user,
        test_type=test_type,
    )
    for question_set_name in ['PHQ2', 'PHQ9', 'GAD2', 'GAD7', 'ASSIST', 'ACE', 'SCHOOL ENV']:  # Adjust as needed
        question_set = QuestionSet.objects.create(
            name=question_set_name,
            test_type=test_type,
            user_submission=user_submission,
        )
        for _ in range(5):  # Generate five submissions for each question set
            Submission.objects.create(
                user_submission=user_submission,
                question_set=question_set,
                question=fake.text(),
                answer=fake.text(),
                score=fake.random_int(min=0, max=27),
                substance=fake.word(),
                specify=fake.word(),
                diagnosis=fake.word(),
            )


# Generate fake data for MeasurementAssist model
for _ in range(10):
    user = CustomUser.objects.order_by('?').first()
    user_submission = UserSubmission.objects.order_by('?').first()
    MeasurementAssist.objects.create(
        user=user,
        user_submission=user_submission,
        alcoholic_measurement=fake.random_element(
            elements=['high risk', 'moderate risk', 'no risk']),
        alcoholic_flag=fake.random_element(
            elements=['red', 'yellow', 'green']),
        tobacco_measurement=fake.random_element(
            elements=['high risk', 'moderate risk', 'no risk']),
        tobacco_flag=fake.random_element(elements=['red', 'yellow', 'green']),
        cannabis_measurement=fake.random_element(
            elements=['high risk', 'moderate risk', 'no risk']),
        cannabis_flag=fake.random_element(elements=['red', 'yellow', 'green']),
        cocaine_measurement=fake.random_element(
            elements=['high risk', 'moderate risk', 'no risk']),
        cocaine_flag=fake.random_element(elements=['red', 'yellow', 'green']),
        amphetamine_measurement=fake.random_element(
            elements=['high risk', 'moderate risk', 'no risk']),
        amphetamine_flag=fake.random_element(
            elements=['red', 'yellow', 'green']),
        inhalants_measurement=fake.random_element(
            elements=['high risk', 'moderate risk', 'no risk']),
        inhalants_flag=fake.random_element(
            elements=['red', 'yellow', 'green']),
        sedatives_measurement=fake.random_element(
            elements=['high risk', 'moderate risk', 'no risk']),
        sedatives_flag=fake.random_element(
            elements=['red', 'yellow', 'green']),
        hallucinogens_measurement=fake.random_element(
            elements=['high risk', 'moderate risk', 'no risk']),
        hallucinogens_flag=fake.random_element(
            elements=['red', 'yellow', 'green']),
        opioids_measurement=fake.random_element(
            elements=['high risk', 'moderate risk', 'no risk']),
        opioids_flag=fake.random_element(elements=['red', 'yellow', 'green']),
        other_measurement=fake.random_element(
            elements=['high risk', 'moderate risk', 'no risk']),
        other_flag=fake.random_element(elements=['red', 'yellow', 'green']),
        other_name=fake.word(),
    )

# Generate fake data for Measurement model
for _ in range(10):
    user = CustomUser.objects.order_by('?').first()
    user_submission = UserSubmission.objects.order_by('?').first()
    Measurement.objects.create(
        user=user,
        user_submission=user_submission,
        gad_measurement=fake.random_element(
            elements=['severe', 'moderate', 'mild', 'minimal']),
        gad_flag=fake.random_element(elements=['red', 'yellow', 'green']),
        phq_measurement=fake.random_element(
            elements=['severe', 'moderately severe', 'moderate', 'mild', 'minimal']),
        phq_flag=fake.random_element(
            elements=['red', 'orange', 'yellow', 'blue', 'green']),
        suicidal_measurement=fake.random_element(
            elements=['nearly everyday', 'more than half the days', 'several days']),
        suicidal_flag=fake.random_element(
            elements=['red', 'orange', 'yellow']),
        ace_measurement=fake.random_element(
            elements=['high risk', 'intermediate risk', 'low risk']),
        ace_flag=fake.random_element(elements=['red', 'yellow', 'green']),
        overall_flag=fake.random_element(elements=['red', 'yellow', 'green']),
    )

# Generate fake data for Agency model
for _ in range(10):
    Agency.objects.create(
        agency_code=fake.random_int(min=1000, max=9999),
        agency_name=fake.company(),
        agency_parent=fake.company_suffix(),
        present_dzongkhag=fake.city(),
        present_gewog=fake.street_name(),
        present_village=fake.street_suffix(),
    )

# Generate fake data for UserAgency model
for _ in range(10):
    user = CustomUser.objects.order_by('?').first()
    agency = Agency.objects.order_by('?').first()
    UserAgency.objects.create(
        user=user,
        agency=agency,
        user_code=fake.random_int(min=1000, max=9999),
        parent_occupation=fake.job(),
        guardian_name=fake.name(),
        guardian_occupation=fake.job(),
        parent_status=fake.word(),
        current_living_with=fake.word(),
        user_role_agency=fake.word(),
        user_class=fake.word(),
        user_stream=fake.word(),
        user_sub_class=fake.word(),
    )

# Generate fake data for CustomUser model
for _ in range(10):
    CustomUser.objects.create(
        username=fake.user_name(),
        identity_number=fake.random_int(min=10000000000, max=29999999999),
        nationality=fake.country(),
        first_name=fake.first_name(),
        middle_name=fake.first_name(),
        last_name=fake.last_name(),
        date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=90),
        gender=fake.random_element(elements=['Male', 'Female']),
        email=fake.email(),
        mob_number=fake.phone_number(),
        father_name=fake.name(),
        mother_name=fake.name(),
        perm_add_village=fake.street_name(),
        perm_add_gewog=fake.street_name(),
        perm_add_dzongkhag=fake.city(),
        ps_add_village=fake.street_name(),
        ps_add_gewog=fake.street_name(),
        ps_add_dzongkhag=fake.city(),
        academy_code=fake.random_int(min=1000, max=9999),
        role=fake.random_element(elements=[
                                 'student', 'clinical_counselor', 'school_counselor', 'admin', 'rd_admin']),
    )
