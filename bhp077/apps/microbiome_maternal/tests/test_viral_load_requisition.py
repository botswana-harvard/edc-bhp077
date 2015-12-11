from django.test import TestCase

from edc.entry_meta_data.models import RequisitionMetaData
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.entry.models.lab_entry import LabEntry
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc_constants.constants import YES, POS, NOT_APPLICABLE

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory
from bhp077.apps.microbiome_maternal.tests.factories import MaternalEligibilityFactory, MaternalVisitFactory
from bhp077.apps.microbiome_maternal.tests.factories import PostnatalEnrollmentFactory
from bhp077.apps.microbiome_maternal.visit_schedule import PostnatalEnrollmentVisitSchedule


class TestViralLoadRequisition(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()

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
