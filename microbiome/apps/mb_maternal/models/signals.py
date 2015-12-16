from django.db import transaction
from django.db.models.signals import post_save
from django.db.utils import IntegrityError
from django.dispatch import receiver

from edc.core.identifier.classes import InfantIdentifier
from edc.subject.appointment.models.appointment import Appointment
from edc.subject.registration.models import RegisteredSubject
from edc.subject.visit_schedule.models.visit_definition import VisitDefinition
from edc_constants.constants import NO, YES, FEMALE, OFF_STUDY, SCHEDULED

from ..models import MaternalOffStudy, MaternalVisit

from .maternal_consent import MaternalConsent
from .maternal_eligibility import MaternalEligibility
from .maternal_eligibility_loss import MaternalEligibilityLoss
from .postnatal_enrollment import PostnatalEnrollment


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
                        gender=FEMALE,
                        subject_type='maternal',
                        registration_datetime=instance.created,
                        user_created=instance.user_created)
                    instance.registered_subject = registered_subject
                    instance.save()


@receiver(post_save, weak=False, dispatch_uid="ineligible_take_off_study")
def ineligible_take_off_study(sender, instance, raw, created, using, **kwargs):
    """If not is_eligible, creates the 1000M visit and sets to off study."""
    if not raw:
        try:
            if not instance.is_eligible:
                with transaction.atomic():
                    report_datetime = instance.report_datetime
                    visit_definition = VisitDefinition.objects.get(code='1000M')
                    appointment = Appointment.objects.get(
                        registered_subject=instance.registered_subject,
                        visit_definition=visit_definition)
                    MaternalVisit.objects.create(
                        appointment=appointment,
                        report_datetime=report_datetime,
                        reason=OFF_STUDY)
        except AttributeError as e:
            if 'is_eligible' not in str(e):
                raise
        except VisitDefinition.DoesNotExist:
            pass
        except Appointment.DoesNotExist:
            pass
        except IntegrityError as e:
            if 'maternalvisit' in str(e):
                with transaction.atomic():
                    maternal_visit = MaternalVisit.objects.get(appointment=appointment)
                    maternal_visit.reason = OFF_STUDY
                    maternal_visit.save()
            else:
                raise


def change_off_study_visit_to_scheduled(instance):
    """Attempts to change the 1000M maternal visit back to scheduled
    from off study."""
    with transaction.atomic():
        try:
            visit_definition = VisitDefinition.objects.get(code='1000M')
            appointment = Appointment.objects.get(
                registered_subject=instance.registered_subject,
                visit_definition=visit_definition)
            maternal_visit = MaternalVisit.objects.get(
                appointment=appointment,
                reason=OFF_STUDY)
            maternal_visit.reason = SCHEDULED
            maternal_visit.save()
        except MaternalVisit.DoesNotExist:
            pass
        except VisitDefinition.DoesNotExist:
            pass
        except Appointment.DoesNotExist:
            pass


@receiver(post_save, weak=False, dispatch_uid="eligible_put_back_on_study")
def eligible_put_back_on_study(sender, instance, raw, created, using, **kwargs):
    """changes the 1000M visit to scheduled from off study if is_eligible."""
    if not raw:
        try:
            if instance.is_eligible:
                MaternalOffStudy.objects.get(registered_subject=instance.registered_subject)
        except AttributeError as e:
            if 'is_eligible' not in str(e) and 'registered_subject' not in str(e):
                raise
        except MaternalOffStudy.DoesNotExist:
            change_off_study_visit_to_scheduled(instance)


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
            instance.registered_subject.study_site = instance.study_site
            instance.registered_subject.save(using=using)


@receiver(post_save, weak=False, dispatch_uid='create_infant_identifier_on_labour_delivery')
def create_infant_identifier_on_labour_delivery(sender, instance, raw, created, using, **kwargs):
    """Creates an identifier for registered infants"""
    if not raw and created:
        try:
            if instance.live_infants_to_register > 0:
                registered_subject = instance.maternal_visit.appointment.registered_subject
                consent = instance.CONSENT_MODEL.objects.get(
                    registered_subject=registered_subject)
                postnatal_enrollment = PostnatalEnrollment.objects.get(
                    registered_subject=consent.registered_subject)
                for infant_order in range(0, instance.live_infants_to_register):
                    infant_identifier = InfantIdentifier(
                        maternal_identifier=registered_subject.subject_identifier,
                        study_site=consent.study_site,
                        birth_order=infant_order,
                        live_infants=postnatal_enrollment.live_infants,
                        live_infants_to_register=instance.live_infants_to_register,
                        user=instance.user_created)
                    infant_identifier.get_identifier()
        except AttributeError:
            pass
