from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

# Import your source models
from screening.models import CaseBasedSubmission, EventBasedSubmission
from gyalsung_users.models import GyalsungUserProfile
from .models import FinalUserSubmission, ServiceAndTreatment

@receiver(post_save, sender=CaseBasedSubmission)
def create_st_for_case_submission(sender, instance, created, **kwargs):
    if created:
        content_type = ContentType.objects.get_for_model(instance)
        ServiceAndTreatment.objects.get_or_create(
            content_type=content_type,
            object_id=instance.id,
            defaults={
                'user': instance.user,
                'date': instance.submission_date.date() if hasattr(instance, 'submission_date') else instance.date.date(),
                # ADDED: Missing default values
                'assessment_status': 'Not Conducted',
                'case_status': 'On Going',
                'counseling': 'Waiting List',
                'updated_by': None
            }
        )

@receiver(post_save, sender=EventBasedSubmission)
def create_st_for_event_submission(sender, instance, created, **kwargs):
    if created:
        content_type = ContentType.objects.get_for_model(instance)
        ServiceAndTreatment.objects.get_or_create(
            content_type=content_type,
            object_id=instance.id,
            defaults={
                'user': instance.user, 
                'date': instance.submission_date.date(),
                # ADDED: Missing default values
                'assessment_status': 'Not Conducted',
                'case_status': 'On Going',
                'counseling': 'Waiting List',
                'updated_by': None
            }
        )

@receiver(post_save, sender=FinalUserSubmission)
def create_st_for_final_submission(sender, instance, created, **kwargs):
    if created:
        content_type = ContentType.objects.get_for_model(instance)
        ServiceAndTreatment.objects.get_or_create(
            content_type=content_type,
            object_id=instance.id,
            defaults={
                'user': instance.user, 
                'date': instance.submission_date.date(),
                # ADDED: Missing default values
                'assessment_status': 'Not Conducted',
                'case_status': 'On Going',
                'counseling': 'Waiting List',
                'updated_by': None
            }
        )

# ADDED: Missing receiver for GyalsungUserProfile
@receiver(post_save, sender=GyalsungUserProfile)
def create_st_for_gyalsung_profile(sender, instance, created, **kwargs):
    if created:
        content_type = ContentType.objects.get_for_model(instance)
        ServiceAndTreatment.objects.get_or_create(
            content_type=content_type,
            object_id=instance.id,
            defaults={
                'user': None,  # GyalsungUserProfile may not have a direct user link
                'date': timezone.now().date(),
                'assessment_status': 'Not Conducted',
                'case_status': 'On Going',
                'counseling': 'Waiting List',
                'updated_by': None
            }
        )