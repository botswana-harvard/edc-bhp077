import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future)
from edc_constants.choices import GENDER


class MaternalScreening(BaseUuidModel):
    """A model completed by the user that confirms basic eligibility. Before or after delivery."""

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,
        ],
        help_text='Date and time of assessing eligibility'
    )

    gender = models.CharField(
        verbose_name='Gender',
        max_length=1,
        choices=GENDER
    )

    age_in_years = models.IntegerField(
        verbose_name='Age in years',
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        db_index=True,
        null=True,
        blank=False,
        help_text="If age is unknown, enter 0. If member is less "
                  "than one year old, enter 1",
    )

    pregnancy_weeks = models.IntegerField(
        verbose_name='If pregnant, how many weeks in to the pregnancy?',
        null=True,
        blank=True,
        help_text='Must be at least 36 weeks pregnant.'
    )

    screening_identifier = models.CharField(
        max_length=36,
        null=True,
        default=None,
        editable=False,
        help_text='Identifier to track registered subject between eligibility pre/post and consent'
    )

    def save(self, *args, **kwargs):
        if not self.screening_identifier:
            self.screening_identifier = uuid.uuid4()
        super(MaternalScreening, self).save(*args, **kwargs)

    class Meta:
        app_label = "microbiome"
        verbose_name = "Maternal Screening"
        verbose_name_plural = "Maternal Screening"
