from django.db import models
from django.core.exceptions import ValidationError
from django_crypto_fields.fields import IdentityField
from edc_base.model.fields import IdentityTypeField

from edc_consent.models import BaseConsent

from ..models import MaternalEligibilityPre
from ..choices import YES_NO_UNKNOWN


class SubjectConsent(BaseConsent):

    citizen = models.CharField(
        verbose_name="Are you a Botswana citizen? ",
        max_length=7,
        choices=YES_NO_UNKNOWN,
        help_text="")

    maternal_eligibility_pre = models.OneToOneField(
        MaternalEligibilityPre,
    )
    
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
        self.matches_maternal_eligibility_pre(self, self.maternal_eligibility_pre)
        # Registered subject values that might have changed are updated in post save signal.
        if self.confirm_identity:
            if self.identity != self.confirm_identity:
                raise ValueError(
                    'Attribute \'identity\' must match attribute \'confirm_identity\'. '
                    'Catch this error on the form'
                )
        #super(SubjectConsent, self).save(*args, **kwargs)

    def matches_maternal_eligibility_pre(self, subject_consent, maternal_eligibility_pre, exception_cls=None):
        """Matches values in this consent against the pre maternal eligibility."""
        exception_cls = exception_cls or ValidationError
        if not maternal_eligibility_pre.is_eligible:
            raise exception_cls('Cannot save a consent when the Maternal Eligibility has not passed.')
        if False:
            raise exception_cls('Subject consent does not match Maternal Pre Elgibility')
        return True

    class Meta:
        app_label = 'microbiome'
