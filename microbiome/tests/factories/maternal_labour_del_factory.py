import factory

from django.utils import timezone

from microbiome.models import MaternalLabourDel


class MaternalLabourDelFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalLabourDel

    delivery_datetime = timezone.now()
    del_time_is_est = 'Yes'
    labour_hrs = '10'
    del_mode = 'Vaginal'
    has_ga = 'Yes'
    ga = 36
    del_hosp = 'PMH'
    has_uterine_tender = 'No'
    labr_max_temp = -1
    has_chorioamnionitis = 'No'
    has_del_comp = 'No'
    live_infants = 1
    live_infants_to_register = 1
    still_borns = 0
