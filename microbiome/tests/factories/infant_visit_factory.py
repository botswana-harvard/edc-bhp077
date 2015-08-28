import factory

from django.utils import timezone
from edc_constants.constants import ALIVE

from microbiome.models import InfantVisit


class InfantVisitFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantVisit

    information_provider = 'Mother'
    study_status = 'onstudy rando ondrug'
    survival_status = ALIVE
    date_last_alive = timezone.now()
