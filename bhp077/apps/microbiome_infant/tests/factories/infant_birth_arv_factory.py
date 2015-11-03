import factory

from django.utils import timezone

from bhp077.apps.microbiome_infant.models import InfantBirthArv
from .infant_visit_factory import InfantVisitFactory
from .infant_birth_factory import InfantBirthFactory


class InfantBirthArvFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantBirthArv

    infant_visit = factory.SubFactory(InfantVisitFactory)
    infant_birth = factory.SubFactory(InfantBirthFactory)
    azt_after_birth = 'Yes'
    azt_dose_date = timezone.now().date()
    azt_additional_dose = 'No'
    sdnvp_after_birth = 'No'
    additional_nvp_doses = 'No'
    azt_discharge_supply = 'No'
    nvp_discharge_supply = 'No'
