import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from edc_base.models import BaseUuidModel
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future)
from edc_constants.choices import GENDER


class MaternalEligibilityPre (BaseUuidModel):
    """A model completed by the user that confirms basic eligibility. Before or after delivery."""

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,
        ],
        help_text='Date and time of assessing eligibility'
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

    gender = models.CharField(
        verbose_name='Gender',
        max_length=1,
        choices=GENDER
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
        super(MaternalEligibilityPre, self).save(*args, **kwargs)

    class Meta:
        app_label = "microbiome"
        verbose_name = "Maternal Eligibility Pre"
        verbose_name_plural = "Maternal Eligibility Pre"
