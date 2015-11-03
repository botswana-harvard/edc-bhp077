import factory

from django.utils import timezone
from edc_constants.constants import YES, NO

from bhp077.apps.microbiome_maternal.models import MaternalLabourDel


class MaternalLabourDelFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalLabourDel

    delivery_datetime = timezone.now()
    del_time_is_est = YES
    labour_hrs = '10'
    del_mode = 'Vaginal'
    has_ga = YES
    ga = 36
    del_hosp = 'PMH'
    has_uterine_tender = NO
    labr_max_temp = -1
    has_chorioamnionitis = NO
    has_del_comp = NO
    live_infants = 1
    live_infants_to_register = 1
    still_borns = 0
