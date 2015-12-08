from django.db import models

from edc.subject.appointment_helper.models import BaseAppointmentMixin
from edc.subject.registration.models import RegisteredSubject
from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future,)
from edc_consent.models import RequiresConsentMixin
from edc_constants.constants import NO, YES, POS, NEG, NOT_APPLICABLE

from .enrollment_mixin import EnrollmentMixin
from .maternal_consent import MaternalConsent
from .maternal_off_study_mixin import MaternalOffStudyMixin
from .postnatal_enrollment import PostnatalEnrollment


class AntenatalEnrollment(EnrollmentMixin, MaternalOffStudyMixin, BaseAppointmentMixin,
                          RequiresConsentMixin, BaseUuidModel):

    CONSENT_MODEL = MaternalConsent

    weeks_base_field = 'gestation_wks'  # for rapid test required calc

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    report_datetime = models.DateTimeField(
        verbose_name="Date and Time of  Antenatal Enrollment",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    gestation_wks = models.IntegerField(
        verbose_name="How many weeks pregnant?",
        help_text=" (weeks of gestation). Eligible if >=36 weeks", )

    objects = models.Manager()

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.is_eligible = self.check_eligibility()
        super(AntenatalEnrollment, self).save(*args, **kwargs)

    def common_fields(self):
        """Returns a list of field names common to postnatal
        and antenatal enrollment models."""
        return [field.name for field in EnrollmentMixin._meta.fields]

    def save_common_fields_to_postnatal_enrollment(self):
        """Saves common field values from Antenatal Enrollment to
        Postnatal Enrollment if Postnatal Enrollment exists.

        Confirms is_eligible does not change value before saving."""
        if self.is_eligible:
            try:
                postnatal_enrollment = PostnatalEnrollment.objects.get(
                    registered_subject=self.registered_subject)
                is_eligible = postnatal_enrollment.is_eligible
                for attrname in self.common_fields():
                    setattr(postnatal_enrollment, attrname, getattr(self, attrname))
                if postnatal_enrollment.check_eligiblity() != is_eligible:
                    raise ValueError(
                        'Eligiblity calculated for Postnatal Enrollment unexpectedly '
                        'changed after updating values from Antenatal Enrollment. '
                        'Got \'is_eligible\' changed from {} to {}.'.format(
                            is_eligible, postnatal_enrollment.is_eligible))
                else:
                    postnatal_enrollment.save()
            except PostnatalEnrollment.DoesNotExist:
                pass

    def check_eligibility(self):
        """Returns True if a mother is eligible."""
        if (self.gestation_wks >= 36 and self.is_diabetic == NO and
                self.on_tb_tx == NO and self.on_hypertension_tx == NO and
                self.will_breastfeed == YES and self.will_remain_onstudy == YES):
            if self.week32_test == YES and self.week32_result in [POS, NEG] and self.evidence_hiv_status == YES:
                return True
            if (self.week32_test == NO and self.rapid_test_done == YES and
                    self.evidence_hiv_status == NO and not self.week32_result):
                return True
            if (self.week32_test == NO and self.rapid_test_done == YES and
                    self.evidence_hiv_status == NOT_APPLICABLE and not self.week32_result):
                return True
            if (self.current_hiv_status == POS and self.evidence_hiv_status == YES and
                    self.valid_regimen == YES and self.valid_regimen_duration == YES):
                return True
            elif self.current_hiv_status == NEG and self.evidence_hiv_status == YES:
                return True
            elif (self.evidence_hiv_status == NO and self.rapid_test_result != POS and
                    self.rapid_test_done == YES):
                return True
        return False

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Antenatal Enrollment'
        verbose_name_plural = 'Antenatal Enrollment'
