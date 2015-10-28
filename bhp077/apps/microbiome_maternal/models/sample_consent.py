from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_consent.models.fields import SampleCollectionFieldsMixin, VulnerabilityFieldsMixin
from edc_consent.models import RequiresConsentMixin
from edc_consent.models.validators import eligible_if_yes
from edc_constants.choices import YES_NO

from .maternal_consent import MaternalConsent


class SampleConsent(SampleCollectionFieldsMixin, RequiresConsentMixin, VulnerabilityFieldsMixin,
                    BaseUuidModel):

    CONSENT_MODEL = MaternalConsent

    consent_benefits = models.CharField(
        verbose_name=("I have explained the purpose of the Infant Gut Microbiome Study"
                      " to the participant. To the best of my knowledge, she understands"
                      " the purpose, procedures, risks and benefits to her and her baby."),
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        null=True,
        blank=False,
        help_text="If no, INELIGIBLE")

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Sample Consent'
        verbose_name_plural = 'Sample Consent'
