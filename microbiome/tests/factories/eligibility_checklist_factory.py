import factory
from django.utils import timezone

from edc_registration.tests.factories import RegisteredSubjectFactory
from ...models import EligibilityChecklist


class EligibilityChecklistFactory(factory.DjangoModelFactory):

    class Meta:
        model = EligibilityChecklist

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    dob = timezone.datetime().date(1997, 10, 10)
    report_datetime = timezone.datetime().today()
    gender = 'M'
    initials = 'NN'
    has_identity = 'Yes'
    guardian = 'N/A'
    citizen = 'Yes'
    disease = 'tuberculosis'
    pregnant_delivered = 'pregnant'
    verbal_hiv_status = 'POS'
    rapid_test_result = 'POS'
