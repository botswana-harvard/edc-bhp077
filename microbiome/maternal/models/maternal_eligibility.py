import uuid
from django.core.urlresolvers import reverse
from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc_constants.choices import YES_NO
from .maternal_eligibility_loss import MaternalEligibilityLoss


class MaternalEligibility (BaseUuidModel):
    """This is the eligibility entry point for all mothers.
    If age eligible or not, an eligibility identifier is created for each mother"""

    eligibility_id = models.CharField(
        verbose_name="Eligibility Identifier",
        max_length=36,
        null=True,
        blank=False,
        editable=False,
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

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False,
        help_text='')

    currently_pregnant = models.CharField(
        verbose_name="Are you currently pregnant?",
        max_length=3,
        choices=YES_NO,
        help_text='')

    recently_delivered = models.CharField(
        verbose_name="Have you recently delivered or had a baby within the past 72 hours?",
        max_length=3,
        choices=YES_NO,
        help_text='')

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.eligibility_id:
            self.eligibility_id = uuid.uuid4()
        self.is_eligible, self.ineligibility = self.mother_is_eligible()
        super(MaternalEligibility, self).save(*args, **kwargs)

    def mother_is_eligible(self):
        '''If age criteria failed, Enrollment loss form will be created.'''
        ineligibility = []
        if self.age_in_years < 18:
            ineligibility.append('Mother is under 18')
        if self.age_in_years > 50:
            ineligibility.append('Mother is too old (>50)')
        return (False if ineligibility else True, ineligibility)

    @property
    def maternal_ineligibility(self):
        reason_ineligible = []
        if self.age_in_years < 18:
            reason_ineligible.append('Under age')
        if self.age_in_years > 50:
            reason_ineligible.append('Over age')
        return reason_ineligible

    @property
    def maternal_eligibility_loss(self):
        try:
            maternal_eligibility_loss = MaternalEligibilityLoss.objects.get(
                maternal_eligibility_id=self.id)
        except MaternalEligibilityLoss.DoesNotExist:
            maternal_eligibility_loss = None
        return maternal_eligibility_loss

    def get_absolute_url(self):
        return reverse('admin:maternal_maternaleligibility_change', args=(self.id,))

    class Meta:
        app_label = 'maternal'
        verbose_name = "Maternal Eligibility"
        verbose_name_plural = "Maternal Eligibility"
