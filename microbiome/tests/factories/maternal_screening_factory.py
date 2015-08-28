import factory

from django.utils import timezone
from edc_constants.constants import FEMALE

from ...models import MaternalScreening


class MaternalScreeningFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalScreening

    report_datetime = timezone.now()
    gender = FEMALE
    age_in_years = 25
