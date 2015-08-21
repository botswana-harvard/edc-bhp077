from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.utils.translation import ugettext as _

from edc_base.model.fields import IdentityTypeField
from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future, dob_not_future)
from edc_registration.models import RegisteredSubject
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models

from django_crypto_fields.fields import IdentityField, FirstnameField
from ..choices import (CHECKLIST_DISEASES, HIVRESULT_CHOICE, PREG_DELIVERED_CHOICE, YES_NO, GENDER,
                       BIRTH_TYPE)
from ..models import MaternalEnrollmentPost

from edc_base.models import BaseUuidModel


class InfantEligibility (BaseUuidModel):
    """A model completed by the user for an infant delivered to an
       HIV +ve mother to determine study eligibility."""

    maternal_enrollment = models.ForeignKey(
        MaternalEnrollmentPost,
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

    infant_hiv_result = models.CharField(
        verbose_name=_("(Interviewer) What is the infant's hiv result?"),
        max_length=30,
        choices=HIVRESULT_CHOICE,
        help_text=_('If the infant is HIV +ve then mother-infant pair is not eligible.')
    )

    objects = models.Manager()

    def save(self, *args, **kwargs):
        super(MaternalEnrollmentPost, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{} ({}) {}/{}".format(self.first_name, self.initials, self.gender, self.age_in_years)

    @property
    def age_in_years(self):
        return True

    class Meta:
        app_label = "microbiome"
        verbose_name = "Eligibility Checklist"
        verbose_name_plural = "Eligibility Checklist"
