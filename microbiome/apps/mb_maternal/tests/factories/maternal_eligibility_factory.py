import factory

from django.utils import timezone

from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from edc_constants.constants import YES, NO

from microbiome.apps.mb_maternal.models import MaternalEligibility


class MaternalEligibilityFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalEligibility

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    report_datetime = timezone.now()
    age_in_years = 26
    currently_pregnant = YES
    recently_delivered = NO
