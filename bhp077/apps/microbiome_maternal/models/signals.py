from django.db.models.signals import post_save
from django.dispatch import receiver

from edc.subject.registration.models import RegisteredSubject
from edc_constants.constants import NO, YES
from .maternal_eligibility import MaternalEligibility
from .maternal_eligibility_loss import MaternalEligibilityLoss
from .maternal_labour_del import MaternalLabourDel
from bhp077.apps.microbiome_maternal.models import (MaternalConsent, MaternalVisit,
                                                    AntenatalEnrollment, PostnatalEnrollment)


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
            maternal_eligibility = MaternalEligibility.objects.get(registered_subject=instance.registered_subject)
            maternal_eligibility.is_consented = True
            if instance.citizen == YES:
                maternal_eligibility.has_passed_consent = True
            elif instance.citizen == NO:
                maternal_eligibility.has_passed_consent = False
            maternal_eligibility.save()


@receiver(post_save, weak=False, dispatch_uid='update_registered_subject_on_post_save')
def update_registered_subject_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Updates an instance of RegisteredSubject on the sender instance.

    Sender instance is a Consent"""
    if not raw:
        if isinstance(instance, MaternalConsent):
            instance.registered_subject.dob = instance.dob
            instance.registered_subject.is_dob_estimated = instance.is_dob_estimated
            instance.registered_subject.gender = instance.gender
            instance.registered_subject.initials = instance.initials
            instance.registered_subject.identity = instance.identity
            instance.registered_subject.identity_type = instance.identity_type
            instance.registered_subject.first_name = instance.first_name
            instance.registered_subject.last_name = instance.last_name
            instance.registered_subject.subject_identifier = instance.subject_identifier
            instance.registered_subject.save(using=using)


@receiver(post_save, weak=False, dispatch_uid='post_save_create_infant_identifier')
def post_save_create_infant_identifier(sender, instance, raw, created, using, **kwarg):
    if isinstance(instance, MaternalLabourDel):
        instance.post_save_create_infant_identifier(created)


@receiver(post_save, weak=False, dispatch_uid="maternal_visit_on_post_save")
def maternal_visit_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Updates maternal scheduled meta data."""
    if not raw:
        if isinstance(instance, MaternalVisit):
            instance.update_scheduled_entry_meta_data()
