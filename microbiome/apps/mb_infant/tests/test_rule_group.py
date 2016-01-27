from edc_registration.models import RegisteredSubject
from edc_meta_data.models import CrfMetaData, RequisitionMetaData
from edc_appointment.models import Appointment
from edc_constants.constants import NEW, YES, POS, MALE, SCHEDULED, UNKEYED, REQUIRED, MISSED_VISIT

from microbiome.apps.mb.constants import INFANT
from microbiome.apps.mb_maternal.tests.factories import (
    MaternalEligibilityFactory, MaternalVisitFactory)
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory

from microbiome.apps.mb_infant.tests.factories import (
    InfantBirthFactory, InfantBirthDataFactory, InfantVisitFactory, InfantFuFactory)

from .base_test_case import BaseTestCase


class TestRuleGroup(BaseTestCase):

    def setUp(self):
        super(TestRuleGroup, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

    def test_infantbirtharv_required_on_postnatal_enrollment_pos(self):
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES)
        self.assertEqual(postnatal_enrollment.enrollment_hiv_status, POS)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='2000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)
        registered_subject_infant = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type=INFANT)
        InfantBirthFactory(
            registered_subject=registered_subject_infant,
            maternal_labour_del=maternal_labour_del)
        appointment = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2000')
        InfantVisitFactory(appointment=appointment, reason=SCHEDULED)
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=UNKEYED,
                crf_entry__app_label='mb_infant',
                crf_entry__model_name='infantbirtharv',
                appointment=appointment).count(), 1)

    def test_congentinal_yes(self):
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject)
        self.assertEqual(postnatal_enrollment.enrollment_hiv_status, POS)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='2000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)
        registered_subject_infant = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type=INFANT)
        InfantBirthFactory(
            registered_subject=registered_subject_infant,
            maternal_labour_del=maternal_labour_del)
        appointment = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2000')
        infant_visit = InfantVisitFactory(appointment=appointment)
        InfantBirthDataFactory(infant_visit=infant_visit)
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=NEW,
                crf_entry__app_label='mb_infant',
                crf_entry__model_name='infantcongenitalanomalies',
                appointment=appointment).count(), 1)

    def test_if_maternal_pos_dna_pcr_required(self):
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES)
        self.assertEqual(postnatal_enrollment.enrollment_hiv_status, POS)
        self.assertTrue(postnatal_enrollment.is_eligible)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=appointment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)
        registered_subject_infant = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type=INFANT)
        InfantBirthFactory(
            registered_subject=registered_subject_infant,
            maternal_labour_del=maternal_labour_del)
        for code in ['2000', '2010', '2030', '2060', '2090', '2120']:
            appointment = Appointment.objects.get(
                registered_subject=registered_subject_infant,
                visit_definition__code=code)
            InfantVisitFactory(
                appointment=appointment,
                reason=SCHEDULED)
            self.assertEqual(RequisitionMetaData.objects.filter(
                entry_status=REQUIRED,
                lab_entry__requisition_panel__name='DNA PCR',
                lab_entry__app_label='mb_lab',
                lab_entry__model_name='infantrequisition',
                appointment=appointment).count(), 1)

    def test_infant_fu_rules(self):
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES)
        self.assertEqual(postnatal_enrollment.enrollment_hiv_status, POS)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='2000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)
        registered_subject_infant = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type=INFANT)
        InfantBirthFactory(
            registered_subject=registered_subject_infant,
            maternal_labour_del=maternal_labour_del)
        appointment = Appointment.objects.get(
            visit_definition__code='2000',
            registered_subject=registered_subject_infant)
        InfantVisitFactory(appointment=appointment)
        appointment = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2010')
        infant_visit = InfantVisitFactory(
            appointment=appointment,
            reason=SCHEDULED)
        InfantFuFactory(infant_visit=infant_visit)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=NEW,
            crf_entry__app_label='mb_infant',
            crf_entry__model_name='infantfuphysical',
            appointment=appointment).count(), 1)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=NEW,
            crf_entry__app_label='mb_infant',
            crf_entry__model_name='infantfudx',
            appointment=appointment).count(), 1)

    def test_infant_visit_circumcision_required(self):
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES)
        self.assertEqual(postnatal_enrollment.enrollment_hiv_status, POS)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='2000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)
        registered_subject_infant = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type=INFANT)
        InfantBirthFactory(
            registered_subject=registered_subject_infant,
            maternal_labour_del=maternal_labour_del,
            gender=MALE)
        appointment = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2000')
        InfantVisitFactory(
            appointment=appointment,
            reason=SCHEDULED)
        appointment = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2010')
        InfantVisitFactory(
            appointment=appointment,
            reason=SCHEDULED)
        appointment = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2030')
        InfantVisitFactory(
            appointment=appointment,
            reason=SCHEDULED)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=UNKEYED,
            crf_entry__app_label='mb_infant',
            crf_entry__model_name='infantcircumcision',
            appointment=appointment).count(), 1)

    def test_infant_visit_missed_at_2030_requires_circumcision_at_2060(self):
        """Test an missed infant visit at 2030 would require a circumcision form at 2060"""
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES)
        self.assertEqual(postnatal_enrollment.enrollment_hiv_status, POS)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='2000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)
        registered_subject_infant = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type=INFANT)
        InfantBirthFactory(
            registered_subject=registered_subject_infant,
            maternal_labour_del=maternal_labour_del,
            gender=MALE)
        appointment = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2000')
        InfantVisitFactory(
            appointment=appointment,
            reason=SCHEDULED)
        appointment = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2010')
        InfantVisitFactory(
            appointment=appointment,
            reason=SCHEDULED)
        appointment = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2030')
        InfantVisitFactory(
            appointment=appointment,
            reason=MISSED_VISIT)
        appointment = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2060')
        InfantVisitFactory(
            appointment=appointment,
            reason=SCHEDULED)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=UNKEYED,
            crf_entry__app_label='mb_infant',
            crf_entry__model_name='infantcircumcision',
            appointment=appointment).count(), 1)
