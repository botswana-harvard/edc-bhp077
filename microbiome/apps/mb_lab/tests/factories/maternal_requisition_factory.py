import factory

from django.utils import timezone

from edc.core.bhp_variables.tests.factories.study_site_factory import StudySiteFactory
from edc_constants.constants import YES
from edc.lab.lab_clinic_api.tests.factories import PanelFactory

from bhp077.apps.microbiome_lab.models import MaternalRequisition
from bhp077.apps.microbiome_maternal.tests.factories import MaternalVisitFactory


class MaternalRequistionFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalRequisition

    report_datetime = timezone.now()
    maternal_visit = factory.SubFactory(MaternalVisitFactory)
    requisition_datetime = timezone.now()
    drawn_datetime = timezone.now() - timezone.timedelta(hours=1)
    panel = factory.SubFactory(PanelFactory)
    is_drawn = YES
    item_type = 'tube'
    item_count_total = 1
    estimated_volume = 5.0
    priority = 'normal'
    study_site = factory.SubFactory(StudySiteFactory)
