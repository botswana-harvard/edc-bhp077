from edc_appointment.models import Appointment
from edc_constants.constants import YES, POS, NOT_APPLICABLE
from edc_meta_data.models import RequisitionMetaData
from edc_meta_data.models.lab_entry import LabEntry

from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory, MaternalVisitFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory

from .base_test_case import BaseTestCase


class TestViralLoadRequisition(BaseTestCase):

    def setUp(self):
        super(TestViralLoadRequisition, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_eligibility.registered_subject
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE)
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)

        def test_viral_load_meta_data_for_pos(self):
            labs = ['Viral Load']
            maternal_visits = ['2000M', '2010M', '2030M', '2060M', '2090M', '2120M']
            for visit in maternal_visits:
                appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                      visit_definition__code=visit)
                visit = MaternalVisitFactory(appointment=appointment)
                for mylab in labs:
                    lab_entry = LabEntry.objects.get(model_name=mylab,
                                                     visit_definition_id=appointment.visit_definition_id)
                    lab_meta_data = RequisitionMetaData.objects.get(lab_entry=lab_entry, appointment=appointment)
                    self.assertEqual(lab_meta_data.entry_status, 'NEW')
