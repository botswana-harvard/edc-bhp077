import factory

from django.utils import timezone

from edc_constants.constants import NO, YES

from microbiome.apps.mb_maternal.models import MaternalPostFu, MaternalPostFuMed

from .lists_factory import ChronicConditionsFactory
from .maternal_visit_factory import MaternalVisitFactory


class MaternalPostFuFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalPostFu

    maternal_visit = factory.SubFactory(MaternalVisitFactory)
    report_datetime = timezone.now()
    weight_measured = YES
    weight_kg = 60.0
    systolic_bp = 120
    diastolic_bp = 80
    chronic_cond_since = NO


class MaternalPostFuMedFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalPostFuMed

    maternal_visit = factory.SubFactory(MaternalVisitFactory)
    report_datetime = timezone.now()
    has_taken_meds = NO
