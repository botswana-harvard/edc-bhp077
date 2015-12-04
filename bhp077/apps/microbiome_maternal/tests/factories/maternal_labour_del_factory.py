import factory

from django.utils import timezone

from edc_constants.constants import YES, NO

from bhp077.apps.microbiome_maternal.models import MaternalLabourDel


class MaternalLabourDelFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalLabourDel

    delivery_datetime = timezone.now()
    delivery_time_estimated = YES
    labour_hrs = '10'
    delivery_time_estimated = YES
    labour_max_temp = 36
    delivery_hospital = 'PMH'
    has_uterine_tender = NO
    labour_max_temp = -1
    has_chorioamnionitis = NO
    delivery_complications = NO
    live_infants_to_register = 1
