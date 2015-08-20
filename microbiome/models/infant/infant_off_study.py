from django.db import models

from edc_base.model.models import BaseUuidModel


class InfantOffStudy():

    infant_visit = models.OneToOneField(InfantVisit)

    report_datetime = models.DateTimeField(
        verbose_name="Visit Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_is_after_consent,
            datetime_not_future,
            ],
        default=datetime.today()
        )

    offstudy_date = models.DateField(
        verbose_name="Off-study Date",
        help_text="")

    reason = models.CharField(
        verbose_name="Please code the primary reason participant taken off-study",
        max_length=115)

    reason_other = models.CharField()

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
