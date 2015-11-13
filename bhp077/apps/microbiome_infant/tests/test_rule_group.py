from django.test import TestCase
from django.utils import timezone

from edc.subject.registration.models import RegisteredSubject
from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc_constants.constants import NEW, YES, NO, POS, NEG, NOT_REQUIRED

from bhp077.apps.microbiome.constants import LIVE
from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_maternal.tests.factories import (MaternalEligibilityFactory, AntenatalEnrollmentFactory,
    MaternalVisitFactory)
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from bhp077.apps.microbiome_maternal.tests.factories import PostnatalEnrollmentFactory, SexualReproductiveHealthFactory
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile, InfantProfile
from bhp077.apps.microbiome_maternal.models import PostnatalEnrollment

from bhp077.apps.microbiome_maternal.visit_schedule import AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule
from bhp077.apps.microbiome_infant.visit_schedule import InfantBirthVisitSchedule
from bhp077.apps.microbiome_infant.tests.factories import InfantBirthFactory, InfantBirthDataFactory, InfantVisitFactory
from bhp077.apps.microbiome_infant.models import InfantBirth

from bhp077.apps.microbiome_lab.models import Panel, AliquotType


class TestRuleGroupInfant(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
            site_lab_profiles.register(InfantProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        AntenatalEnrollmentVisitSchedule().build()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()
        InfantBirthVisitSchedule().build()

        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject


    def model_options(self, app_label, model_name, appointment):
        model_options = {}
        model_options.update(
            entry__app_label=app_label,
            entry__model_name=model_name,
            appointment=appointment)
        return model_options

    def test_hiv_status_pos_on_postnatal_enrollment(self):
        """
        """
        post = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            verbal_hiv_status=POS,
            evidence_hiv_status=YES,
        )

        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M'
        )
        maternal_visit = MaternalVisitFactory(appointment=appointment)

        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)

        registered_subject_infant = RegisteredSubject.objects.get(
            subject_type='infant', relative_identifier=self.registered_subject.subject_identifier
        )
        InfantBirthFactory(
            registered_subject=registered_subject_infant,
            maternal_labour_del=maternal_labour_del,
        )
        appointment = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2000'
        )
        InfantVisitFactory(appointment=appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **self.model_options(
            app_label='microbiome_infant', model_name='infantbirtharv', appointment=appointment
        )).count(), 1)

    def test_infant_birth_male(self):
        """
        """
        post = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            verbal_hiv_status=POS,
            evidence_hiv_status=YES,
        )

        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M'
        )
        maternal_visit = MaternalVisitFactory(appointment=appointment)

        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)

        registered_subject_infant = RegisteredSubject.objects.get(
            subject_type='infant', relative_identifier=self.registered_subject.subject_identifier
        )
        InfantBirthFactory(
            registered_subject=registered_subject_infant,
            maternal_labour_del=maternal_labour_del,
            gender='M',
        )
        for code in ['2030', '2060', '2090', '2120']:
            appointment = Appointment.objects.get(
                registered_subject=registered_subject_infant, visit_definition__code=code
            )
            InfantVisitFactory(appointment=appointment)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **self.model_options(
                app_label='microbiome_infant', model_name='infantcircumcision', appointment=appointment
            )).count(), 1)

    def test_congentinal_yes(self):
        """
        """
        post = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
        )

        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M'
        )
        maternal_visit = MaternalVisitFactory(appointment=appointment)

        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)

        registered_subject_infant = RegisteredSubject.objects.get(
            subject_type='infant', relative_identifier=self.registered_subject.subject_identifier
        )
        infant_birth = InfantBirthFactory(
            registered_subject=registered_subject_infant,
            maternal_labour_del=maternal_labour_del,
        )

        appointment = Appointment.objects.get(
            registered_subject=registered_subject_infant, visit_definition__code='2000'
        )

        infant_visit = InfantVisitFactory(appointment=appointment)

        InfantBirthDataFactory(infant_visit=infant_visit, infant_birth=infant_birth)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **self.model_options(
            app_label='microbiome_infant', model_name='infantcongenitalanomalies', appointment=appointment
        )).count(), 1)

    def test_maternal_pos_with_evidence(self):
        """
        """
        post = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            verbal_hiv_status=POS,
            evidence_hiv_status=YES,
        )

        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M'
        )
        maternal_visit = MaternalVisitFactory(appointment=appointment)

        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)

        registered_subject_infant = RegisteredSubject.objects.get(
            subject_type='infant', relative_identifier=self.registered_subject.subject_identifier
        )
        InfantBirthFactory(
            registered_subject=registered_subject_infant,
            maternal_labour_del=maternal_labour_del,
        )

        for code in ['2000']: #, '2010', '2030', '2060', '2090', '2120'
            appointment = Appointment.objects.get(
                registered_subject=registered_subject_infant, visit_definition__code=code
            )
            InfantVisitFactory(appointment=appointment)
            self.assertEqual(RequisitionMetaData.objects.filter(
                entry_status=NEW, lab_entry__requisition_panel__name='DNA PCR',
                lab_entry__app_label='microbiome_lab',
                lab_entry__model_name='infantrequisition',
                appointment=appointment
            ).count(), 1)
