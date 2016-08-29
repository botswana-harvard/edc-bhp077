import factory

from django.utils import timezone

from microbiome.apps.mb_infant.models import InfantFeeding

from edc_constants.constants import NO, NOT_APPLICABLE

from .infant_visit_factory import InfantVisitFactory


class InfantFeedingFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantFeeding

    infant_visit = factory.SubFactory(InfantVisitFactory)
    other_feeding = NO
    formula_intro_occur = NOT_APPLICABLE
    formula_intro_date = None
    took_formula = NOT_APPLICABLE
    is_first_formula = None
    water = NOT_APPLICABLE
    juice = NOT_APPLICABLE
    cow_milk = NOT_APPLICABLE
    other_milk = NOT_APPLICABLE
    other_milk_animal = NOT_APPLICABLE
    milk_boiled = NOT_APPLICABLE
    cereal_porridge = NOT_APPLICABLE
    solid_liquid = NOT_APPLICABLE
    rehydration_salts = NOT_APPLICABLE
    water_used = NOT_APPLICABLE
    water_used_other = None
    ever_breastfeed = NOT_APPLICABLE
    complete_weaning = NOT_APPLICABLE
    weaned_completely = NOT_APPLICABLE
    most_recent_bm = None
    times_breastfed = '<1 per week'
