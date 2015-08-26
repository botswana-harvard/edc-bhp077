import factory
from django.utils import timezone

from ...models import MaternalScreening


class MaternalScreeningFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalScreening

    report_datetime = timezone.now()
    gender = 'F'
    age_in_years = 25
