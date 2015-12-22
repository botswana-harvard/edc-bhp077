from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from edc.core.identifier.classes import InfantIdentifier
from edc.subject.registration.models import RegisteredSubject
from edc_visit_schedule.models.visit_definition import VisitDefinition
from edc_appointment.models.appointment import Appointment
from edc_constants.constants import FEMALE, OFF_STUDY, SCHEDULED, SCREENED, CONSENTED

from ..models import MaternalOffStudy, MaternalVisit

from .maternal_consent import MaternalConsent
from .maternal_eligibility import MaternalEligibility
from .maternal_eligibility_loss import MaternalEligibilityLoss
from .postnatal_enrollment import PostnatalEnrollment
from microbiome.apps.mb.constants import INFANT


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
    """Creates and or updates the Registered Subject instance for this subject if maternal eligibility passes.

    If participant is consented, does nothing

    * If registered subject does not exist, it will be created and some attrs
      updated from the MaternalEligibility;
    * If registered subject already exists will update some attrs from the MaternalEligibility;
    * If registered subject and consent already exist, does nothing.

    Note: This is the ONLY place RegisteredSubject is created in this project."""
    if not raw:
        if isinstance(instance, MaternalEligibility):
            if instance.is_eligible:
                try:
                    registered_subject = RegisteredSubject.objects.get(
                        screening_identifier=instance.eligibility_id)
                    MaternalConsent.objects.get(registered_subject=registered_subject)
                except RegisteredSubject.DoesNotExist:
                    registered_subject = RegisteredSubject.objects.create(
                        created=instance.created,
                        first_name='Mother',
                        gender=FEMALE,
                        registration_status=SCREENED,
                        screening_datetime=instance.report_datetime,
                        screening_identifier=instance.eligibility_id,
                        screening_age_in_years=instance.age_in_years,
                        subject_type='maternal',
                        user_created=instance.user_created)
                    instance.registered_subject = registered_subject
                    instance.save()
                except MaternalConsent.DoesNotExist:
                    registered_subject.first_name = 'Mother'
                    registered_subject.gender = FEMALE
                    registered_subject.registration_status = SCREENED
                    registered_subject.screening_datetime = instance.report_datetime
                    registered_subject.screening_identifier = instance.eligibility_id
                    registered_subject.screening_age_in_years = instance.age_in_years
                    registered_subject.subject_type = 'maternal'
                    registered_subject.user_modified = instance.user_modified
                    registered_subject.save()


@receiver(post_save, weak=False, dispatch_uid="ineligible_take_off_study")
def ineligible_take_off_study(sender, instance, raw, created, using, **kwargs):
    """If not is_eligible, creates the 1000M visit and sets to off study."""
    if not raw:
        try:
            if not instance.is_eligible:
                report_datetime = instance.report_datetime
                visit_definition = VisitDefinition.objects.get(code=instance.off_study_visit_code)
                appointment = Appointment.objects.get(
                    registered_subject=instance.registered_subject,
                    visit_definition=visit_definition)
                maternal_visit = MaternalVisit.objects.get(appointment=appointment)
                if maternal_visit.reason != OFF_STUDY:
                    maternal_visit.reason = OFF_STUDY
                    maternal_visit.save()
        except MaternalVisit.DoesNotExist:
            MaternalVisit.objects.create(
                appointment=appointment,
                report_datetime=report_datetime,
                reason=OFF_STUDY)
        except AttributeError as e:
            if 'is_eligible' not in str(e) and 'off_study_visit_code' not in str(e):
                raise
        except VisitDefinition.DoesNotExist:
            pass
        except Appointment.DoesNotExist:
            pass


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
    """Update maternal_eligibility consented flag and update matching attrs on
    RegisteredSubject."""
    if not raw:
        if isinstance(instance, MaternalConsent):
            maternal_eligibility = MaternalEligibility.objects.get(
                registered_subject=instance.registered_subject)
            maternal_eligibility.is_consented = True
            # don't trigger the signal
            maternal_eligibility.save(update_fields=['is_consented'])
            instance.registered_subject.registration_datetime = instance.consent_datetime
            instance.registered_subject.registration_status = CONSENTED
            instance.registered_subject.registration_identifier = instance.pk
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
    """Creates an identifier for the registered infant.

    RegisteredSubject.objects.create( is called by InfantIdentifier

    Only one infant per mother is allowed."""
    if not raw and created:
        try:
            if instance.live_infants_to_register == 1:
                maternal_registered_subject = instance.maternal_visit.appointment.registered_subject
                maternal_consent = instance.CONSENT_MODEL.objects.get(
                    registered_subject=maternal_registered_subject)
                postnatal_enrollment = PostnatalEnrollment.objects.get(
                    registered_subject=maternal_consent.registered_subject)
                with transaction.atomic():
                    infant_identifier = InfantIdentifier(
                        maternal_identifier=maternal_registered_subject.subject_identifier,
                        study_site=maternal_consent.study_site,
                        birth_order=0,
                        live_infants=postnatal_enrollment.live_infants,
                        live_infants_to_register=instance.live_infants_to_register,
                        user=instance.user_created)
                    infant_identifier.get_identifier()
                with transaction.atomic():
                    # TODO: InfantIdentifier class above does not update all registered subject
                    # attributes correctly.
                    infant_registered_subject = RegisteredSubject.objects.get(
                        relative_identifier=maternal_registered_subject.subject_identifier)
                    infant_registered_subject.registration_datetime = instance.delivery_datetime
                    infant_registered_subject.subject_type = INFANT
                    infant_registered_subject.first_name = 'No Name'
                    infant_registered_subject.initials = None
                    infant_registered_subject.registration_status = 'DELIVERED'
                    infant_registered_subject.save()
        except AttributeError:
            pass
