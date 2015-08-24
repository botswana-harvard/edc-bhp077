import factory
from django.utils import timezone

from edc_registration.tests.factories import RegisteredSubjectFactory
from ...models import MaternalEligibilityPre


class MaternalEligibilityPreFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalEligibilityPre

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    dob = timezone.datetime(1997, 10, 10).date()
    report_datetime = timezone.now()
    gender = 'M'
    initials = 'NN'
    has_identity = 'Yes'
    citizen = 'Yes'
    disease = 'N/A'
    pregnancy_weeks = 37
    currently_pregnant = 'pregnant'
    verbal_hiv_status = 'POS'
    rapid_test_result = 'POS'
