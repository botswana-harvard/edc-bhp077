import pprint
from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from edc.subject.registration.models import RegisteredSubject

from .maternal_eligibility import MaternalEligibility
from .maternal_consent import MaternalConsent
from .maternal_eligibility_loss import MaternalEligibilityLoss


@receiver(post_save, weak=False, dispatch_uid="maternal_eligibility_on_post_save")
def maternal_eligibility_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Creates a ClinicEnrollmentLoss instance if not eligible."""
    if not raw:
        if isinstance(instance, MaternalEligibility):
            if not instance.is_eligible:
                try:
                    maternal_eligibility_loss = MaternalEligibilityLoss.objects.get(
                        maternal_eligibility_id=instance.id)
                    maternal_eligibility_loss.report_datetime = instance.report_datetime
                    maternal_eligibility_loss.reason_ineligible = instance.ineligibility
                    maternal_eligibility_loss.user_modified = instance.user_modified
                    maternal_eligibility_loss.save()
                except MaternalEligibilityLoss.DoesNotExist:
                    MaternalEligibilityLoss.objects.create(
                        maternal_eligibility_id=instance.id,
                        report_datetime=instance.report_datetime,
                        reason_ineligible=instance.ineligibility,
                        user_created=instance.user_created,
                        user_modified=instance.user_modified)
            else:
                MaternalEligibilityLoss.objects.filter(maternal_eligibility_id=instance.id).delete()


@receiver(post_save, weak=False, dispatch_uid="criteria_passed_create_registered_subject")
def criteria_passed_create_registered_subject(sender, instance, raw, created, using, **kwargs):
    """Creates a Registered Subject ONLY if maternal eligibility is passed."""
    if not raw:
        if isinstance(instance, MaternalEligibility):
            if instance.is_eligible:
                if not instance.registered_subject:
                    registered_subject = RegisteredSubject.objects.create(
                        created=instance.created,
                        first_name='Mother',
                        gender='F',
                        subject_type='maternal',
                        registration_datetime=instance.created,
                        user_created=instance.user_created)
                    instance.registered_subject = registered_subject
                    instance.save()


@receiver(post_save, weak=False, dispatch_uid="maternal_consent_on_post_save")
def maternal_consent_on_post_save(sender, instance, raw, created, using, **kwargs):
    """This will update the is_consented boolean on maternal eligibility"""
    if not raw:
        if isinstance(instance, MaternalConsent):
            pass
#             maternal_eligibility = MaternalEligibility.objects.get(registered_subject=instance.registered_subject)
#             maternal_eligibility.is_consented = True
#             maternal_eligibility.save(update_fields='is_consented')
