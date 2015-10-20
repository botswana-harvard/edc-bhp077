from django.db import models

# from edc_base.model.validators import (
#     datetime_not_before_study_start, datetime_not_future)
from edc_constants.choices import YES_NO, YES

from .infant_visit import InfantVisit
from .infant_scheduled_visit_model import InfantScheduledVisitModel


class InfantOffStudy(InfantScheduledVisitModel):

    infant_visit = models.OneToOneField(InfantVisit)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
#         validators=[
#             datetime_not_before_study_start,
#             datetime_not_future,
#         ],
    )

    offstudy_date = models.DateField(
        verbose_name="Off-study Date",
    )

    reason = models.CharField(
        verbose_name="Please code the primary reason participant taken off-study",
        max_length=115)

    reason_other = models.CharField(
        max_length=100)

    has_scheduled_data = models.CharField(
        max_length=10,
        verbose_name='Are scheduled data being submitted on the off-study date?',
        choices=YES_NO,
        default=YES,
        help_text='')

    comment = models.TextField(
        max_length=250,
        verbose_name="Comments:",
        blank=True,
        null=True)

    class Meta:
        app_label = "infant"
        verbose_name = "Infant Off-Study"
