from django.db import models

from edc.device.sync.models import BaseSyncUuidModel
from edc.subject.registration.models import RegisteredSubject
from edc_appointment.models import AppointmentMixin
from edc_base.audit_trail import AuditTrail
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future,)
from edc_consent.models import RequiresConsentMixin

from ..managers import AntenatalEnrollmentManager

from .enrollment_helper import EnrollmentError
from .enrollment_mixin import EnrollmentMixin
from .maternal_consent import MaternalConsent
from .maternal_off_study_mixin import MaternalOffStudyMixin
from .postnatal_enrollment import PostnatalEnrollment


class AntenatalEnrollment(EnrollmentMixin, MaternalOffStudyMixin, AppointmentMixin,
                          RequiresConsentMixin, BaseSyncUuidModel):

    CONSENT_MODEL = MaternalConsent

    weeks_base_field = 'gestation_wks'  # for rapid test required calc

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    gestation_wks = models.IntegerField(
        verbose_name="How many weeks pregnant?",
        help_text=" (weeks of gestation). Eligible if >=36 weeks", )

    objects = AntenatalEnrollmentManager()

    history = AuditTrail()

    def natural_key(self):
        return (self.registered_subject,)

    def save(self, *args, **kwargs):
        self.update_common_fields_to_postnatal_enrollment()
        super(AntenatalEnrollment, self).save(*args, **kwargs)

    @property
    def off_study_visit_code(self):
        """Returns the visit code for the off-study visit if eligibility criteria fail."""
        return '1000M'

    def update_common_fields_to_postnatal_enrollment(self):
        """Updates common field values from Antenatal Enrollment to
        Postnatal Enrollment if Postnatal Enrollment exists.

        Confirms is_eligible does not change value before saving."""
        if self.id and self.is_eligible:
            try:
                postnatal_enrollment = PostnatalEnrollment.objects.get(
                    registered_subject=self.registered_subject)
                is_eligible = postnatal_enrollment.is_eligible
                for attrname in self.common_fields():
                    setattr(postnatal_enrollment, attrname, getattr(self, attrname))
                if postnatal_enrollment.check_eligiblity() != is_eligible:
                    raise EnrollmentError(
                        'Eligiblity calculated for Postnatal Enrollment unexpectedly '
                        'changed after updating values from Antenatal Enrollment. '
                        'Got \'is_eligible\' changed from {} to {}.'.format(
                            is_eligible, postnatal_enrollment.is_eligible))
                else:
                    postnatal_enrollment.save()
            except PostnatalEnrollment.DoesNotExist:
                pass

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = 'Antenatal Enrollment'
        verbose_name_plural = 'Antenatal Enrollment'
