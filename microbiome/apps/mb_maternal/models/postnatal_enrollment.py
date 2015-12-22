from django.db import models, transaction
from django.db.models import get_model

from edc.device.sync.models import BaseSyncUuidModel
from edc.subject.registration.models import RegisteredSubject
from edc_appointment.models import AppointmentMixin
from edc_base.audit_trail import AuditTrail
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future,)
from edc_consent.models import RequiresConsentMixin
from edc_constants.choices import YES_NO

from ..managers import PostnatalEnrollmentManager
from ..maternal_choices import LIVE_STILL_BIRTH

from .enrollment_mixin import EnrollmentMixin
from .maternal_consent import MaternalConsent
from .maternal_off_study_mixin import MaternalOffStudyMixin
from microbiome.apps.mb_maternal.models.enrollment_helper import EnrollmentError


class PostnatalEnrollment(EnrollmentMixin, MaternalOffStudyMixin, AppointmentMixin,
                          RequiresConsentMixin, BaseSyncUuidModel):

    CONSENT_MODEL = MaternalConsent

    weeks_base_field = 'gestation_wks_delivered'  # for rapid test required calc

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    postpartum_days = models.IntegerField(
        verbose_name="How many days postpartum?",
        help_text="If more than 3days, not eligible")

    vaginal_delivery = models.CharField(
        verbose_name="Was this a vaginal delivery?",
        choices=YES_NO,
        max_length=3,
        help_text="INELIGIBLE if NO")

    gestation_wks_delivered = models.IntegerField(
        verbose_name="How many weeks after gestation was the child born?",
        help_text="ineligible if premature or born before 37weeks")

    delivery_status = models.CharField(
        verbose_name="Was this a live or still birth?",
        choices=LIVE_STILL_BIRTH,
        max_length=15,
        help_text='if still birth, not eligible')

    live_infants = models.IntegerField(
        verbose_name="How many live infants?",
        null=True,
        blank=True)

    objects = PostnatalEnrollmentManager()

    history = AuditTrail()

    def natural_key(self):
        return (self.report_datetime, self.registered_subject.natural_key())

    def save(self, *args, **kwargs):
        self.update_with_common_fields_from_antenatal_enrollment()
        self.is_eligible_if_antenatal_exists_or_raise()
        super(PostnatalEnrollment, self).save(*args, **kwargs)

    def get_registration_datetime(self):
        return self.report_datetime

    def is_eligible_if_antenatal_exists_or_raise(self, exception_cls=None):
        exception_cls = exception_cls or EnrollmentError
        AntenatalEnrollment = get_model('mb_maternal', 'antenatalenrollment')
        with transaction.atomic():
            try:
                antenatal_enrollment = AntenatalEnrollment.objects.get(
                    registered_subject=self.registered_subject)
                if not antenatal_enrollment.is_eligible:
                    raise EnrollmentError(
                        'Subject was determined ineligible at Antenatal '
                        'Enrollment on {}. Cannot continue.'.format(
                            antenatal_enrollment.report_datetime))
            except AntenatalEnrollment.DoesNotExist:
                pass

    @property
    def off_study_visit_code(self):
        """Returns the visit code for the off-study visit if eligibility criteria fail.

        Returns either 1000M or, if Antenatal Enrollment exists, 2000M."""
        try:
            AntenatalEnrollment = get_model('mb_maternal', 'antenatalenrollment')
            AntenatalEnrollment.objects.get(registered_subject=self.registered_subject)
            off_study_visit_code = '2000M'
        except AntenatalEnrollment.DoesNotExist:
            off_study_visit_code = '1000M'
        return off_study_visit_code

    def update_with_common_fields_from_antenatal_enrollment(self):
        """Updates common field values from Antenatal Enrollment to
        this instance if not already set.

        Only updates if AntenatalEnrollment.is_eligible=True."""
        AntenatalEnrollment = get_model('mb_maternal', 'antenatalenrollment')
        try:
            antenatal_enrollment = AntenatalEnrollment.objects.get(
                registered_subject=self.registered_subject,
                is_eligible=True)
            for attrname in self.common_fields():
                if not getattr(self, attrname):
                    setattr(self, attrname, getattr(antenatal_enrollment, attrname))
        except AntenatalEnrollment.DoesNotExist:
            pass

    @property
    def antenatal_enrollment(self):
        """Is this ever used??"""
        AntenatalEnrollment = get_model('mb_maternal', 'antenatalenrollment')
        try:
            return AntenatalEnrollment.objects.get(registered_subject=self.registered_subject)
        except AntenatalEnrollment.DoesNotExist:
            return None
        return None

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = 'Postnatal Enrollment'
        verbose_name_plural = 'Postnatal Enrollment'
