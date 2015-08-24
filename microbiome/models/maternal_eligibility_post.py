from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from edc_base.models import BaseUuidModel
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future)
from edc_registration.models import RegisteredSubject

from ..choices import BIRTH_TYPE


class MaternalEligibilityPost (BaseUuidModel):
    """A model completed strictly after delivery to ensure the mother can
       continue with the study."""

    registered_subject = models.OneToOneField(
        RegisteredSubject,
        null=True,
        blank=True,
        help_text=''
    )

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,
        ],
        help_text='Date and time of assessing eligibility'
    )

    days_post_natal = models.IntegerField(
        verbose_name="How many days postnatal? ",
        help_text="if >34 days, ineligible",
        validators=[
            MaxValueValidator(34),
            MinValueValidator(0)
        ]
    )

    weeks_of_gestation = models.IntegerField(
        verbose_name="How many weeks of gestation was this pregnancy?",
        help_text="If gestation is 36 weeks or less, then not eligible.",
    )

    type_of_birth = models.CharField(
        verbose_name="How was the infant(s) delivered? ",
        max_length=10,
        choices=BIRTH_TYPE,
        help_text="If cesarean section, then not eligible."
    )

    live_infants = models.IntegerField(
        verbose_name="How many live infants did the mother deliver?",
        help_text="If zero live then not eligible.",
    )

    objects = models.Manager()

    def __str__(self):
        return "{} ({}) {}/{}".format(self.first_name, self.initials, self.gender, self.age_in_years)

    class Meta:
        app_label = "microbiome"
        verbose_name = "Maternal Eligibility Post"
        verbose_name_plural = "Maternal Eligibility Post"
