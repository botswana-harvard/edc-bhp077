import factory
from django.utils import timezone

from edc_constants.constants import YES, NO

from microbiome.apps.mb_maternal.models import ReproductiveHealth

from .maternal_visit_factory import MaternalVisitFactory


class ReproductiveHealthFactory(factory.DjangoModelFactory):

    class Meta:
        model = ReproductiveHealth

    report_datetime = timezone.now()
    maternal_visit = factory.SubFactory(MaternalVisitFactory)
    more_children = YES
    contraceptive_measure = YES
    uses_contraceptive = NO
    srh_referral = YES
