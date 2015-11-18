import factory

from django.utils import timezone
from edc_constants.constants import NO

from bhp077.apps.microbiome_maternal.models import MaternalPostFu

from .lists_factory import ChronicConditionsFactory
from .maternal_visit_factory import MaternalVisitFactory


class MaternalPostFuFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalPostFu

    maternal_visit = factory.SubFactory(MaternalVisitFactory)
    report_datetime = timezone.now()
    mother_weight = NO
    enter_weight = ''
    systolic_bp = 120
    diastolic_bp = 80
    has_chronic_cond = NO
    chronic_cond = [factory.SubFactory(ChronicConditionsFactory)]
