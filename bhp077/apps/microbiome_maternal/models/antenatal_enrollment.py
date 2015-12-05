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


class AntenatalEnrollment(EnrollmentMixin, MaternalOffStudyMixin, BaseAppointmentMixin,
                          RequiresConsentMixin, BaseUuidModel):

    CONSENT_MODEL = MaternalConsent

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

    antenatal_eligible = models.BooleanField(
        default=False,
        editable=False)

    objects = models.Manager()

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.antenatal_eligible = self.eligible_for_postnatal
        super(AntenatalEnrollment, self).save(*args, **kwargs)

    @property
    def weeks_base(self):
        return self.gestation_wks

    @property
    def postnatal_enrollment(self):
        try:
            PostnatalEnrollment = models.get_model('microbiome_maternal', 'postnatalenrollment')
            return PostnatalEnrollment.objects.get(registered_subject=self.registered_subject)
        except PostnatalEnrollment.DoesNotExist:
            return False

    def update_postnatal(self, postnatal_enrollment):

        if postnatal_enrollment:
            postnatal_enrollment.is_diabetic = self.is_diabetic
            postnatal_enrollment.on_tb_tx = self.on_tb_tx
            postnatal_enrollment.on_hypertension_tx = self.on_hypertension_tx
            postnatal_enrollment.will_breastfeed = self.will_breastfeed
            postnatal_enrollment.will_remain_onstudy = self.will_remain_onstudy
            postnatal_enrollment.week32_result = self.week32_result
            postnatal_enrollment.week32_test_date = self.week32_test_date
            postnatal_enrollment.current_hiv_status = self.current_hiv_status
            postnatal_enrollment.valid_regimen = self.valid_regimen
            postnatal_enrollment.evidence_hiv_status = self.evidence_hiv_status
            postnatal_enrollment.rapid_test_done = self.rapid_test_done
            postnatal_enrollment.rapid_test_date = self.rapid_test_date
            postnatal_enrollment.rapid_test_result = self.rapid_test_result
            postnatal_enrollment.valid_regimen = self.valid_regimen
            postnatal_enrollment.save()

    @property
    def eligible_for_postnatal(self):
        """Returns True if a mother is eligible for postnatalenrollment."""
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
