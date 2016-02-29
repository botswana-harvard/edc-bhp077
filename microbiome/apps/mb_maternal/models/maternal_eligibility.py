from uuid import uuid4

from django.db import models
from django.db.models import get_model

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc_constants.choices import YES_NO
from edc_constants.constants import NO
from edc_registration.models import RegisteredSubject
from edc_sync.models import SyncModelMixin

from microbiome.apps.mb.constants import MIN_AGE_OF_CONSENT, MAX_AGE_OF_CONSENT

from ..managers import MaternalEligibilityManager


class MaternalEligibility (SyncModelMixin, BaseUuidModel):
    """ A model completed by the user to test and capture the result of the pre-consent eligibility checks.

    This model has no PII."""

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    eligibility_id = models.CharField(
        verbose_name="Eligibility Identifier",
        max_length=36,
        default=None,
        editable=False)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        help_text='Date and time of assessing eligibility')

    age_in_years = models.IntegerField(
        verbose_name='What is the age of the participant?')

    has_omang = models.CharField(
        verbose_name="Do you have an OMANG?",
        max_length=3,
        choices=YES_NO)

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    currently_pregnant = models.CharField(
        verbose_name="Are you currently pregnant?",
        max_length=3,
        choices=YES_NO)

    recently_delivered = models.CharField(
        verbose_name="Have you recently delivered or had a baby within the past 72 hours?",
        max_length=3,
        choices=YES_NO)

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

    objects = MaternalEligibilityManager()

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.set_uuid_for_eligibility_if_none()
        self.is_eligible, error_message = self.check_eligibility()
        self.ineligibility = error_message  # error_message not None if is_eligible is False
        super(MaternalEligibility, self).save(*args, **kwargs)

    def check_eligibility(self):
        """Returns a tuple (True, None) if mother is eligible otherwise (False, error_messsage) where
        error message is the reason for eligibility test failed."""
        error_message = []
        if self.age_in_years < MIN_AGE_OF_CONSENT:
            error_message.append('Mother is under {}'.format(MIN_AGE_OF_CONSENT))
        if self.age_in_years > MAX_AGE_OF_CONSENT:
            error_message.append('Mother is too old (>{})'.format(MAX_AGE_OF_CONSENT))
        if self.has_omang == NO:
            error_message.append('Not a citizen')
        is_eligible = False if error_message else True
        return (is_eligible, ','.join(error_message))

    def __unicode__(self):
        return "{0} ({1})".format(self.eligibility_id, self.age_in_years)

    def natural_key(self):
        return (self.eligibility_id, self.report_datetime, )

    @property
    def maternal_eligibility_loss(self):
        MaternalEligibilityLoss = get_model('mb_maternal', 'MaternalEligibilityLoss')
        try:
            maternal_eligibility_loss = MaternalEligibilityLoss.objects.get(
                maternal_eligibility_id=self.id)
        except MaternalEligibilityLoss.DoesNotExist:
            maternal_eligibility_loss = None
        return maternal_eligibility_loss

    def set_uuid_for_eligibility_if_none(self):
        if not self.eligibility_id:
            self.eligibility_id = str(uuid4())

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = "Maternal Eligibility"
        verbose_name_plural = "Maternal Eligibility"
