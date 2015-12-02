from django.db import models

from edc_constants.choices import YES_NO, POS_NEG

from .maternal_scheduled_visit_model import MaternalScheduledVisitModel
from .maternal_consent import MaternalConsent


class RapidTestResult(MaternalScheduledVisitModel):

    """ A model completed by the user on the mother's rapid test result. """

    CONSENT_MODEL = MaternalConsent

    process_rapid_test = models.CharField(
        verbose_name="Was a rapid test processed?",
        choices=YES_NO,
        max_length=3,
        help_text='')

    date_of_rapid_test = models.DateField(
        verbose_name="Date of rapid test",
        null=True,
        blank=True,
        help_text='If rapid test processed, we need to know the date')

    rapid_test_result = models.CharField(
        verbose_name="What is the rapid test result?",
        choices=POS_NEG,
        null=True,
        blank=True,
        max_length=15)

    comments = models.CharField(
        verbose_name="Comment",
        max_length=250,
        blank=True,
        null=True)

    def get_result_datetime(self):
        return self.report_datetime

    def get_test_code(self):
        return 'HIV'

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Rapid Test Result'
        verbose_name_plural = 'Rapid Test Result'
