import factory
from django.utils import timezone

from ...models import MaternalEligibilityPre


class MaternalEligibilityPreFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalEligibilityPre

    report_datetime = timezone.now()
    gender = 'F'
    age_in_years = 25
