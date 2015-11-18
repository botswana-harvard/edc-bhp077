import factory

from django.conf import settings
from django.utils import timezone

from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from edc_constants.constants import YES

from bhp077.apps.microbiome_maternal.models import SampleConsent


class SampleConsentFactory(factory.DjangoModelFactory):

    class Meta:
        model = SampleConsent

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    report_datetime = timezone.now()
    language = settings.LANGUAGES,
    may_store_samples = YES,
    is_literate = YES,
    consent_benefits = YES
