from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc_constants.choices import YES_NO, YES_NO_UNKNOWN
from edc_registration.models import RegisteredSubject

# from ..list.diseases_at_enrollment import DiseasesAtEnrollment


class MaternalEligibility (BaseUuidModel):
    """This is the main eligibility which determines
    the mothers enrollment type.
    e.g. antenatal or postnatal"""

    registered_subject = models.OneToOneField(
        RegisteredSubject,
        null=True,
        blank=True,
        help_text='')

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,
        ],
        help_text='Date and time of assessing eligibility')

    age_in_years = models.IntegerField(
        verbose_name='What is the age of the participant?')

    citizen = models.CharField(
        verbose_name="Are you a Botswana citizen? ",
        max_length=7,
        choices=YES_NO_UNKNOWN,
        help_text="if NO, ineligible")

#     disease = models.ManyToManyField(
#         DiseasesAtEnrollment,
#         verbose_name="Do you currently have any of the following diseases?",
#         max_length=15,
#         help_text="If participant has any of the diseases, then not eligible.")
    is_diabetic = models.CharField(
        verbose_name='Are you diabetic?',
        choices=YES_NO,
        max_length=3)

    has_tb = models.CharField(
        verbose_name="Do you have tubercolosis",
        choices=YES_NO,
        max_length=3)

    breastfeed_for_a_year = models.CharField(
        verbose_name='Are you willing to breast-feed your child for a whole year?',
        choices=YES_NO,
        max_length=3)

    instudy_for_a_year = models.CharField(
        verbose_name="Are you willing to remain in the study during the infants first year of life",
        choices=YES_NO,
        max_length=3)

    currently_pregnant = models.CharField(
        verbose_name="Are you currently pregnant?",
        max_length=3,
        choices=YES_NO,
        help_text='')

    objects = models.Manager()

    class Meta:
        app_label = "microbiome"
        verbose_name = "Maternal Eligibility"
        verbose_name_plural = "Maternal Eligibility"
