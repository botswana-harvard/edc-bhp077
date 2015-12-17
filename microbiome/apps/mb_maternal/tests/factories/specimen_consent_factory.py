import factory

from django.conf import settings
from django.utils import timezone

from edc_constants.constants import YES

from microbiome.apps.mb_maternal.models import SpecimenConsent


class SpecimenConsentFactory(factory.DjangoModelFactory):

    class Meta:
        model = SpecimenConsent

    consent_datetime = timezone.now()
    language = settings.LANGUAGES
    may_store_samples = YES
    is_literate = YES
