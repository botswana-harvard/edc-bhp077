from edc_constants.choices import YES, NO, POS, NEG

from ..maternal_choices import LIVE
from .base_enrollment import Enrollment
from .antenatal_enrollment import AntenatalEnrollment
from ..managers import PostnatalEnrollmentManager


class PostnatalEnrollment(Enrollment):

    objects = PostnatalEnrollmentManager()

    def save(self, *args, **kwargs):
        self.enrollment_type = 'postnatal'
        self.postnatal_enrollemet_eligible = self.postnatal_eligible
        super(PostnatalEnrollment, self).save(*args, **kwargs)

    def get_registration_datetime(self):
        return self.report_datetime

    def number_of_weeks_after_tests(self):
        value = self.gestation_before_birth - self.weeks_between(self.date_of_test, self.report_datetime.date())
        return value

    def validate_rapid_test_required_or_not_required(self):
        return self.number_of_weeks_after_tests >= 32

    @property
    def postnatal_eligible(self):
        """Returns true if the participant is eligible."""
        if (self.breastfeed_for_a_year == YES and self.on_tb_treatment == NO and
                self.on_hypertension_treatment == NO and self.is_diabetic == NO and
                self.instudy_for_a_year == YES and self.postpartum_days <= 3 and self.delivery_type == YES and
                self.live_or_still_birth == LIVE and self.gestation_before_birth >= 37):
            if (self.verbal_hiv_status == POS and self.evidence_hiv_status == YES and self.valid_regimen == YES and
                    self.valid_regimen_duration == YES):
                return True
            elif (self.verbal_hiv_status == POS and self.evidence_hiv_status == NO and
                    self.rapid_test_result == POS and self.valid_regimen == YES and self.valid_regimen_duration == YES):
                return True
            elif self.verbal_hiv_status == NEG and self.evidence_hiv_status == NO and self.rapid_test_result == NEG:
                return True
            elif self.verbal_hiv_status == NEG and self.evidence_hiv_status == YES:
                return True
            elif (self.verbal_hiv_status in ['Never tested for HIV', 'Unknown', 'Refused to answer'] and
                    self.rapid_test_result == NEG):
                return True
        return False

    @property
    def antenatal_enrollment(self):
        try:
            return AntenatalEnrollment.objects.get(registered_subject=self.registered_subject)
        except AntenatalEnrollment.DoesNotExist:
            return None
        return None

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Postnatal Enrollment'
        verbose_name_plural = 'Postnatal Enrollment'
        proxy = True
