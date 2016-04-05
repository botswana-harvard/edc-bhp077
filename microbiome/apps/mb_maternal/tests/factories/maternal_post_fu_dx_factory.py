import factory

from edc_constants.constants import YES
from edc_code_lists.models import WcsDxAdult

from microbiome.apps.mb_maternal.models import MaternalPostFuDx, MaternalPostFuDxT

from .maternal_visit_factory import MaternalVisitFactory

from ...maternal_choices import DX


class WcsDxAdultFactory():
    class Meta:
        model = WcsDxAdult

    list_ref = None


class MaternalPostFuDxFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalPostFuDx

    maternal_visit = factory.SubFactory(MaternalVisitFactory)
    hospitalized_since = YES
    new_dx_since = YES
    new_wcs_dx_since = YES
# maternal_factory = MaternalPostFuDxFactory()
# who = WcsDxAdultFactory()
# maternal_factory.who.add(who)


class MaternalPostFuDxTFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalPostFuDxT

    maternal_post_fu_med = factory.SubFactory(MaternalPostFuDxFactory)
    post_fu_dx = DX[0][0]
