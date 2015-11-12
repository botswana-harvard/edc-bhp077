import factory

from django.utils import timezone

from edc_constants.constants import YES

from bhp077.apps.microbiome_infant.models import InfantBirthArv
from .infant_visit_factory import InfantVisitFactory
from .infant_birth_factory import InfantBirthFactory
from ...models import InfantBirthData


class InfantBirthDataFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantBirthData

    congenital_anomalities = YES
    infant_birth_weight = '3'
    infant_length = '50'
    head_circumference = '10'
