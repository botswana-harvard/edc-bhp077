from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone
from django_crypto_fields.fields import IdentityField

from edc_base.model.fields import IdentityTypeField
from edc_consent.models import BaseConsent
from edc_constants.choices import YES_NO_UNKNOWN, NO
from .maternal_eligibility import MaternalEligibility
from .identifiers import MaternalIdentifier


class MaternalConsent(BaseConsent):

    maternal_eligibility = models.OneToOneField(
        MaternalEligibility,
        verbose_name="Mother'\s Eligibility")

    citizen = models.CharField(
        verbose_name="Are you a Botswana citizen? ",
        max_length=7,
        choices=YES_NO_UNKNOWN,
        help_text="")

    identity = IdentityField(
        verbose_name="Identity number (OMANG, etc)",
        unique=True,
        null=True,
        blank=True,
        help_text="Use Omang, Passport number, driver's license number or Omang receipt number"
    )
    confirm_identity = IdentityField(
        verbose_name="Confirm identity",
        unique=True,
        null=True,
        blank=True,
        help_text="re-enter the identity number from above. DO NOT COPY AND PASTE"
    )

    identity_type = IdentityTypeField(
        null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.subject_identifier = MaternalIdentifier().identifier
        self.identity_match()
        super(MaternalConsent, self).save(*args, **kwargs)

    def identity_match(self):
        if self.confirm_identity:
            if self.identity != self.confirm_identity:
                raise ValueError(
                    'Attribute \'identity\' must match attribute \'confirm_identity\'. '
                )
        return True

    @property
    def age_in_years(self):
        return relativedelta(timezone.now().date(), self.dob).years

    @property
    def is_eligible(self):
        """Evaluates maternal eligibility criteria"""
        if not (self.age_in_years < 18):
            return False
        elif self.citizen == NO:
            return False
        else:
            return True

    class Meta:
        app_label = 'microbiome'
        verbose_name = 'Maternal Consent'
        verbose_name_plural = 'Maternal Consent'
