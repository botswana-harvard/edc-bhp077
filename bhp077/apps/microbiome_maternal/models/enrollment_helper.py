from edc_constants.constants import NO, YES, UNKNOWN, POS, NEG, IND, NOT_APPLICABLE, SEROCONVERSION, NEVER, DWTA
from dateutil.relativedelta import relativedelta
from bhp077.apps.microbiome.constants import LIVE
from django.core.exceptions import ValidationError


class EnrollmentError(Exception):
    pass


class EnrollmentHelper(object):

    def __init__(self, instance):
        self._enrollment_hiv_status = None
        self.date_at_32wks = None
        self.instance = instance
        self.enrollment = self.instance._meta.verbose_name
        for field in self.instance._meta.fields:
            try:
                setattr(self, field.name, getattr(self.instance, field.name))
            except AttributeError:
                pass
        try:
            self.gestational_age = self.gestation_wks
            self.passes_basic_criteria = self.antenatal_criteria
        except AttributeError:
            self.gestational_age = self.gestation_wks_delivered
            self.passes_basic_criteria = self.postnatal_criteria
        self.is_eligible = self.is_eligible_for_enrollment()

    def is_eligible_for_enrollment(self):
        """Returns True is all eligibility criteria passes."""
        is_eligible = False
        if self.passes_basic_criteria():
            if (self.enrollment_hiv_status == POS and self.valid_regimen == YES and
                    self.valid_regimen_duration == YES):
                is_eligible = True
            elif self.enrollment_hiv_status == NEG:
                is_eligible = True
        return is_eligible

    def antenatal_criteria(self):
        """Returns True if basic criteria, not including HIV status,
        is met for antenatal enrollment."""
        if (self.gestation_wks >= 36 and self.no_chronic_conditions() and
                self.will_breastfeed == YES and self.will_remain_onstudy == YES):
            return True
        return False

    def postnatal_criteria(self):
        """Returns True if basic criteria, not including HIV status,
        is met for postnatal enrollment."""
        if (self.delivery_status == LIVE and self.gestation_wks_delivered >= 37 and
                self.no_chronic_conditions() and
                self.postpartum_days <= 3 and
                self.vaginal_delivery == YES and
                self.will_breastfeed == YES and
                self.will_remain_onstudy == YES):
            return True
        return False

    @property
    def enrollment_hiv_status(self):
        """Returns the maternal HIV status at enrollment based on valid combinations
        expected from the form otherwise raises a EnrollmentError.

        Note: the EnrollmentError should never be excepted!!"""
        if not self._enrollment_hiv_status:
            if self.evidence_hiv_status == YES:
                self._enrollment_hiv_status = self.hiv_status_with_evidence()
            elif self.evidence_hiv_status in [NO, NOT_APPLICABLE]:
                self._enrollment_hiv_status = self.hiv_status_with_without_evidence()
            if not self._enrollment_hiv_status:
                raise EnrollmentError(
                    'Unable to determine maternal hiv status at enrollment. '
                    'Got current_hiv_status={}, evidence_hiv_status={}, '
                    'rapid_test_done={}, rapid_test_result={}'.format(
                        self.current_hiv_status,
                        self.evidence_hiv_status,
                        self.rapid_test_done,
                        self.rapid_test_result))
        return self._enrollment_hiv_status

    def hiv_status_with_evidence(self):
        """Returns the hiv status if evidence is available or None."""
        hiv_status = None
        if self.evidence_hiv_status == YES:
            if self.hiv_status_on_or_after_32wk() == POS:
                hiv_status = POS
            elif self.hiv_status_on_or_after_32wk() == NEG:
                hiv_status = NEG
            elif self.current_hiv_status == POS and self.rapid_test_done in [NO, NOT_APPLICABLE]:
                hiv_status = POS
            elif self.current_hiv_status == NEG and self.rapid_test_done in [NO, NOT_APPLICABLE]:
                hiv_status = UNKNOWN
            elif (self.current_hiv_status == POS and self.rapid_test_done == YES and
                    self.rapid_test_result == POS):
                hiv_status = POS
            elif (self.current_hiv_status == NEG and
                    self.rapid_test_done == YES and self.rapid_test_result == NEG):
                hiv_status = NEG
            elif (self.current_hiv_status == NEG and
                    self.rapid_test_done == YES and self.rapid_test_result == POS):
                hiv_status = SEROCONVERSION
            elif (self.current_hiv_status == NEG and
                    self.rapid_test_done == YES and self.rapid_test_result == IND):
                hiv_status = IND
        return hiv_status

    def hiv_status_with_without_evidence(self):
        """Returns the hiv status if evidence is not available or None."""
        if self.evidence_hiv_status in [NO, NOT_APPLICABLE]:
            if (self.current_hiv_status == POS and self.rapid_test_done == YES and
                    self.rapid_test_result == POS):
                hiv_status = POS
            elif (self.current_hiv_status == POS and self.rapid_test_done == NO and
                    self.rapid_test_result is None):
                hiv_status = UNKNOWN
            elif (self.current_hiv_status in [NEG, NEVER, UNKNOWN, DWTA] and self.rapid_test_done == YES and
                    self.rapid_test_result == NEG):
                hiv_status = NEG
            elif (self.current_hiv_status in [NEG, NEVER, UNKNOWN, DWTA] and self.rapid_test_done == YES and
                    self.rapid_test_result == POS):
                hiv_status = SEROCONVERSION
            elif (self.current_hiv_status in [NEG, NEVER, UNKNOWN, DWTA] and self.rapid_test_done == NO and
                    self.rapid_test_result is None):
                hiv_status = UNKNOWN
        return hiv_status

    def hiv_status_on_or_after_32wk(self, exception_cls=None):
        """Returns the maternal status on or after week 32 gestational age or None."""
        hiv_status = None
        exception_cls = exception_cls or ValidationError
        if self.week32_test == YES and self.week32_test_date:
            if not self.test_date_is_on_or_after_32wks():
                raise exception_cls(
                    'Test date is not on or after 32 weeks gestational age.')
            elif self.week32_result == POS and self.current_hiv_status == POS:
                hiv_status = POS
            elif self.week32_result == NEG and self.current_hiv_status == NEG:
                hiv_status = NEG
        return hiv_status

    def test_date_is_on_or_after_32wks(self):
        """Returns True if the test date is on or after 32 weeks gestational age."""
        self.date_at_32wks = self.report_datetime.date() - relativedelta(weeks=self.gestational_age - 32)
        if self.rapid_test_date:
            if self.week32_test_date > self.rapid_test_date:
                raise ValidationError('Rapid test date cannot precede test date on or after 32 weeks')
        return self.week32_test_date >= self.date_at_32wks

    def no_chronic_conditions(self):
        """Returns True if subject has no chronic conditions."""
        return (self.is_diabetic == NO and
                self.on_tb_tx == NO and
                self.on_hypertension_tx == NO)
