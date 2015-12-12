from django.test import TestCase
from django.utils import timezone
 
from edc.core.bhp_variables.tests.factories.study_site_factory import StudySiteFactory
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.lab.lab_clinic_api.tests.factories import PanelFactory
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.subject.code_lists.models import WcsDxAdult
from edc_constants.choices import YES, NO
from edc.entry_meta_data.models.requisition_meta_data import RequisitionMetaData
 
from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from bhp077.apps.microbiome_lab.models.aliquot import AliquotType
from bhp077.apps.microbiome_list.models.chronic_conditions import ChronicConditions
from bhp077.apps.microbiome_maternal.forms import (MaternalPostFuForm, MaternalPostFuDxForm)
from bhp077.apps.microbiome_maternal.visit_schedule import PostnatalEnrollmentVisitSchedule
from bhp077.apps.microbiome_maternal.tests.factories import (PostnatalEnrollmentFactory, MaternalVisitFactory,
                        MaternalEligibilityFactory, MaternalConsentFactory)

from ..forms import MaternalRequisitionForm
from ..models import Panel


class TestMaternalRequisitionForm(TestCase):
    """Test eligibility of a mother for postnatal followup."""

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()
        self.study_site = StudySiteFactory()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject,
                                                       study_site=self.study_site)
        self.registered_subject = self.maternal_consent.registered_subject
        self.postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            will_breastfeed=YES
        )
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='2000M')
        self.panel = Panel.objects.get(name='Breast Milk (Storage)')
        self.aliquot_type = AliquotType.objects.get(alpha_code='WB')
        self.data = {
            'maternal_visit': None,
            'requisition_datetime': timezone.now(),
            'is_drawn': NO,
            'reason_not_drawn': 'collection_failed',
            'drawn_datetime': '',
            'site': self.study_site.id,
            'panel': self.panel.id,
            'aliquot_type': self.aliquot_type.id,
            'item_type': 'tube',
            'item_count_total': '',
            'estimated_volume': '',
            'priority': '',
            'comments': '',
        }

    def test_visit_reason_unscheduled(self):
        maternal_visit = MaternalVisitFactory(appointment=self.appointment, reason="unscheduled")
        self.data['maternal_visit'] = maternal_visit.id
        self.data['is_drawn'] = YES
        self.data['drawn_datetime'] = timezone.now() - timezone.timedelta(hours=1)
        self.data['item_count_total'] = 1
        self.data['estimated_volume'] = 5.0
        self.data['reason_not_drawn'] = ''
        self.data['priority'] = 'normal'
        form = MaternalRequisitionForm(data=self.data)
        self.assertTrue(form.is_valid())
        errors = ''.join(form.errors.get('__all__'))
