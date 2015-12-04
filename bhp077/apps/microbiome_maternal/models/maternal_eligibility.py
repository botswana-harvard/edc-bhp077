import uuid

from django.db import models

from edc.subject.registration.models import RegisteredSubject
from edc_base.model.models import BaseUuidModel
from edc_base.audit_trail import AuditTrail
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc_constants.choices import YES_NO
from edc_constants.constants import NO

from .maternal_consent import MaternalConsent


class MaternalEligibility (BaseUuidModel):
    """ This is the eligibility entry point for all mothers.
    If age eligible or not, an eligibility identifier is created for each mother. """

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

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

    has_omang = models.CharField(
        verbose_name="Do you have an OMANG?",
        max_length=3,
        choices=YES_NO,
        help_text='')

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
    # is updated via signal once subject is consented
    is_consented = models.BooleanField(
        default=False,
        editable=False)
    # updated by signal on saving consent, is determined by participant citizenship
    has_passed_consent = models.BooleanField(
        default=False,
        editable=False)

    objects = models.Manager()

    history = AuditTrail()

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
        if self.has_omang == 'No':
            ineligibility.append('Not a citizen')
        return (False if ineligibility else True, ineligibility)

    def __unicode__(self):
        return "{0} ({1})".format(self.eligibility_id, self.age_in_years)

    @property
    def maternal_ineligibility(self):
        reason_ineligible = []
        if self.age_in_years < 18:
            reason_ineligible.append('Under age')
        if self.age_in_years > 50:
            reason_ineligible.append('Over age')
        if self.has_omang == NO:
            reason_ineligible.append('Not a citizen')
        return reason_ineligible

    @property
    def maternal_eligibility_loss(self):
        from .maternal_eligibility_loss import MaternalEligibilityLoss
        try:
            maternal_eligibility_loss = MaternalEligibilityLoss.objects.get(
                maternal_eligibility_id=self.id)
        except MaternalEligibilityLoss.DoesNotExist:
            maternal_eligibility_loss = None
        return maternal_eligibility_loss

    @property
    def mothers_consent(self):
        try:
            mothers_consent = MaternalConsent.objects.get(registered_subject=self.registered_subject)
        except MaternalConsent.DoesNotExist:
            mothers_consent = None
        return mothers_consent

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = "Maternal Eligibility"
        verbose_name_plural = "Maternal Eligibility"
