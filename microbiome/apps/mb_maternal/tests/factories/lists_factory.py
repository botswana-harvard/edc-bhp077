import factory

from edc_constants.constants import NOT_APPLICABLE

from microbiome.apps.mb_list.models import Supplements, ChronicConditions, HealthCond


class SupplementsFactory(factory.DjangoModelFactory):

    name = NOT_APPLICABLE
    short_name = NOT_APPLICABLE
    display_index = 10
    version = '1.0'

    class Meta:
        model = Supplements


class HealthCondFactory(factory.DjangoModelFactory):

    name = NOT_APPLICABLE
    short_name = NOT_APPLICABLE
    display_index = 20
    version = '1.0'

    class Meta:
        model = HealthCond


class ChronicConditionsFactory(factory.DjangoModelFactory):

    name = NOT_APPLICABLE
    short_name = NOT_APPLICABLE
    display_index = 20
    version = '1.0'

    class Meta:
        model = ChronicConditions
