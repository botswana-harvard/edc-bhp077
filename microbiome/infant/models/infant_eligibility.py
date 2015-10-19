from django.db import models
from django.utils.translation import ugettext as _

from edc_base.model.validators import (datetime_not_before_study_start, datetime_not_future)
from edc_base.model.models import BaseUuidModel
from edc_constants.constants import NEG, POS

from edc_constants.choices import POS_NEG_ONLY

from microbiome.maternal.models import MaternalEligibility


class InfantEligibility (BaseUuidModel):
    """A model completed by the user for an infant delivered to an
       HIV +ve mother to determine study eligibility."""

    maternal_eligibility_post = models.ForeignKey(
        MaternalEligibility,
        help_text=''
    )

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        null=True,
        blank=True,
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,
        ],
        help_text='Date and time of assessing eligibility'
    )

    infant_hiv_result = models.CharField(
        verbose_name=_("(Interviewer) What is the infant's hiv result?"),
        null=True,
        blank=True,
        max_length=30,
        choices=POS_NEG_ONLY,
        help_text=_('If the infant is HIV +ve then mother-infant pair is not eligible.')
    )

    objects = models.Manager()

    def save(self, *args, **kwargs):
        super(InfantEligibility, self).save(*args, **kwargs)

#     def __str__(self):
#         return "{} ({}) {}/{}".format(self.first_name, self.initials, self.gender, self.age_in_years)

    @property
    def is_resulted(self):
        if self.infant_hiv_result in [POS, NEG]:
            return True
        return False

    @property
    def is_eligible(self):
        if self.infant_hiv_result == NEG:
            return True
        return False

    class Meta:
        app_label = "infant"
        verbose_name = "Infant Eligibility"
        verbose_name_plural = "Infant Eligibility"
