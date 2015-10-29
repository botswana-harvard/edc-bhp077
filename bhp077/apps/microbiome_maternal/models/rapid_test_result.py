from django.db import models

from edc_constants.choices import YES_NO_NA, POS_NEG
from edc_constants.constants import NOT_APPLICABLE

from .maternal_scheduled_visit_model import MaternalScheduledVisitModel


class RapidTestResult(MaternalScheduledVisitModel):

    process_rapid_test = models.CharField(
        verbose_name="Was a rapid test processed?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default=NOT_APPLICABLE,
        max_length=15,
        help_text=('Remember, rapid test is for HIV -VE, UNTESTED, UNKNOWN, REFUSED-to-ANSWER'
                   'verbal responses'))

    date_of_rapid_test = models.DateField(
        verbose_name="Date of rapid test",
        null=True,
        blank=True)

    rapid_test_result = models.CharField(
        verbose_name="What is the rapid test result?",
        choices=POS_NEG,
        max_length=15,
        null=True,
        blank=True,)

    def get_result_datetime(self):
        return self.report_datetime

    def get_test_code(self):
        return 'HIV'

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Rapid Test Result'
        verbose_name_plural = 'Rapid Test Result'
