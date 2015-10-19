from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone

from edc_base.model.fields import IdentityTypeField
from edc_base.model.fields.custom_fields import OmangField
from edc_consent.models.base_consent import BaseConsent
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_consent.models.fields import PersonalFieldsMixin, VulnerabilityFieldsMixin
from edc_constants.choices import YES_NO_UNKNOWN, NO
# from .identifiers import MaternalIdentifier


class MaternalConsent(BaseConsent, PersonalFieldsMixin, VulnerabilityFieldsMixin, BaseUuidModel):

    citizen = models.CharField(
        verbose_name="Are you a Botswana citizen? ",
        max_length=7,
        choices=YES_NO_UNKNOWN,
        help_text="")

    identity = OmangField(
        verbose_name="Identity number (OMANG, etc)",
        unique=True,
        null=True,
        blank=True,
        help_text="Use Omang, Passport number, driver's license number or Omang receipt number"
    )
    confirm_identity = OmangField(
        verbose_name="Confirm identity",
        unique=True,
        null=True,
        blank=True,
        help_text="re-enter the identity number from above. DO NOT COPY AND PASTE"
    )

    identity_type = IdentityTypeField(
        null=True)
# 
#     def save(self, *args, **kwargs):
#         if not self.id:
#             self.subject_identifier = MaternalIdentifier().identifier
#         self.identity_match()
#         super(MaternalConsent, self).save(*args, **kwargs)

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
        app_label = 'maternal'
        verbose_name = 'Maternal Consent'
        verbose_name_plural = 'Maternal Consent'
