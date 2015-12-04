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

    weeks_of_gestation = models.IntegerField(
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
        return self.weeks_of_gestation

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
            postnatal_enrollment.on_tb_treatment = self.on_tb_treatment
            postnatal_enrollment.on_hypertension_treatment = self.on_hypertension_treatment
            postnatal_enrollment.breastfeed_for_a_year = self.breastfeed_for_a_year
            postnatal_enrollment.instudy_for_a_year = self.instudy_for_a_year
            postnatal_enrollment.week32_result = self.week32_result
            postnatal_enrollment.verbal_hiv_status = self.verbal_hiv_status
            postnatal_enrollment.valid_regimen = self.valid_regimen
            postnatal_enrollment.evidence_hiv_status = self.evidence_hiv_status
            postnatal_enrollment.process_rapid_test = self.process_rapid_test
            postnatal_enrollment.date_of_rapid_test = self.date_of_rapid_test
            postnatal_enrollment.rapid_test_result = self.rapid_test_result
            postnatal_enrollment.valid_regimen = self.valid_regimen
            postnatal_enrollment.save()

    @property
    def eligible_for_postnatal(self):
        """Returns True if a mother is eligible for postnatalenrollment."""
        if (self.weeks_of_gestation >= 36 and self.is_diabetic == NO and
                self.on_tb_treatment == NO and self.on_hypertension_treatment == NO and
                self.breastfeed_for_a_year == YES and self.instudy_for_a_year == YES):
            if self.week32_test == YES and self.week32_result in [POS, NEG] and self.evidence_hiv_status == YES:
                return True
            if (self.week32_test == NO and self.process_rapid_test == YES and
                    self.evidence_hiv_status == NO and not self.week32_result):
                return True
            if (self.week32_test == NO and self.process_rapid_test == YES and
                    self.evidence_hiv_status == NOT_APPLICABLE and not self.week32_result):
                return True
            if (self.verbal_hiv_status == POS and self.evidence_hiv_status == YES and
                    self.valid_regimen == YES and self.valid_regimen_duration == YES):
                return True
            elif self.verbal_hiv_status == NEG and self.evidence_hiv_status == YES:
                return True
            elif (self.evidence_hiv_status == NO and self.rapid_test_result != POS and
                    self.process_rapid_test == YES):
                return True
        return False

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Antenatal Enrollment'
        verbose_name_plural = 'Antenatal Enrollment'
