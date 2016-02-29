import factory

from django.utils import timezone

from edc_constants.constants import NO, YES
from edc_constants.choices import DRUG_ROUTE

from microbiome.apps.mb.choices import MEDICATIONS
from microbiome.apps.mb_maternal.models import MaternalPostFu, MaternalPostFuMed, MaternalPostFuMedItems

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
    chronic_since = NO


class MaternalPostFuMedFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalPostFuMed

    maternal_visit = factory.SubFactory(MaternalVisitFactory)
    report_datetime = timezone.now()
    has_taken_meds = NO


class MaternalPostFuMedItemsFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalPostFuMedItems

    maternal_post_fu_med = factory.SubFactory(MaternalPostFuMedFactory)
    date_first_medication = timezone.now().date()
    medication = MEDICATIONS[0][0]
    drug_route = DRUG_ROUTE[0][0]
