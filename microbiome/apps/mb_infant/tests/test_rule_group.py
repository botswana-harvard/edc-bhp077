from datetime import date
from django.utils import timezone

from edc_registration.models import RegisteredSubject
from edc_meta_data.models import CrfMetaData, RequisitionMetaData
from edc_appointment.models import Appointment
from edc_constants.constants import (
    NEW, YES, POS, NEG, MALE, SCHEDULED, UNKEYED, REQUIRED,
    MISSED_VISIT, KEYED, NOT_REQUIRED, NOT_APPLICABLE)

from microbiome.apps.mb.constants import INFANT
from microbiome.apps.mb_maternal.tests.factories import (
    MaternalEligibilityFactory, MaternalVisitFactory)
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory

from microbiome.apps.mb_infant.tests.factories import (
    InfantBirthFactory, InfantBirthDataFactory, InfantVisitFactory, InfantFuFactory, InfantArvProphFactory)

from ...mb.constants import NO_MODIFICATIONS, DISCONTINUED
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

    def test_infant_arv_proph_required_from_2010(self):
        """Test that infant arv proph is required from 2010 visit"""
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES)
        self.assertEqual(postnatal_enrollment.enrollment_hiv_status, POS)
        maternal_appointment_1000M = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        MaternalVisitFactory(appointment=maternal_appointment_1000M)
        maternal_appointment_2000M = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='2000M')
        maternal_visit_2000M = MaternalVisitFactory(appointment=maternal_appointment_2000M)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit_2000M)
        registered_subject_infant = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type=INFANT)
        InfantBirthFactory(
            registered_subject=registered_subject_infant,
            maternal_labour_del=maternal_labour_del)
        infant_appointment_2000 = Appointment.objects.get(
            visit_definition__code='2000',
            registered_subject=registered_subject_infant)
        InfantVisitFactory(appointment=infant_appointment_2000)
        self.assertFalse(CrfMetaData.objects.filter(
            entry_status=NOT_REQUIRED,
            crf_entry__app_label='mb_infant',
            crf_entry__model_name='infantarvproph',
            appointment=infant_appointment_2000).exists())
        infant_appointment_2010 = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2010')
        InfantVisitFactory(
            appointment=infant_appointment_2010,
            reason=SCHEDULED)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=UNKEYED,
            crf_entry__app_label='mb_infant',
            crf_entry__model_name='infantarvproph',
            appointment=infant_appointment_2010).count(), 1)

    def test_infant_arv_proph_not_required_from_2010(self):
        """Test that infant arv proph is required from 2010 visit"""
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            valid_regimen=NOT_APPLICABLE,
            valid_regimen_duration=NOT_APPLICABLE,
            rapid_test_done=YES,
            rapid_test_date=timezone.now(),
            rapid_test_result=NEG)
        self.assertEqual(postnatal_enrollment.enrollment_hiv_status, NEG)
        maternal_appointment_1000M = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        MaternalVisitFactory(appointment=maternal_appointment_1000M)
        maternal_appointment_2000M = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='2000M')
        maternal_visit_2000M = MaternalVisitFactory(appointment=maternal_appointment_2000M)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit_2000M)
        registered_subject_infant = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type=INFANT)
        InfantBirthFactory(
            registered_subject=registered_subject_infant,
            maternal_labour_del=maternal_labour_del)
        infant_appointment_2000 = Appointment.objects.get(
            visit_definition__code='2000',
            registered_subject=registered_subject_infant)
        InfantVisitFactory(appointment=infant_appointment_2000)
        self.assertFalse(CrfMetaData.objects.filter(
            entry_status=NOT_REQUIRED,
            crf_entry__app_label='mb_infant',
            crf_entry__model_name='infantarvproph',
            appointment=infant_appointment_2000).exists())
        infant_appointment_2010 = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2010')
        InfantVisitFactory(
            appointment=infant_appointment_2010,
            reason=SCHEDULED)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=NOT_REQUIRED,
            crf_entry__app_label='mb_infant',
            crf_entry__model_name='infantarvproph',
            appointment=infant_appointment_2010).count(), 1)

    def test_infant_arv_proph_required_till_discontinued_1(self):
        """Test if infant arv proph is not required if arv status of infant is discontinued"""
        registered_subject_infant = self.infant_arv_proph_setup()
        infant_appointment_2030 = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2030')
        infant_visit_2030 = InfantVisitFactory(
            appointment=infant_appointment_2030,
            reason=SCHEDULED)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=UNKEYED,
            crf_entry__app_label='mb_infant',
            crf_entry__model_name='infantarvproph',
            appointment=infant_appointment_2030).count(), 1)
        InfantArvProphFactory(infant_visit=infant_visit_2030, prophylatic_nvp=YES, arv_status=DISCONTINUED)
        infant_appointment_2060 = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2060')
        InfantVisitFactory(
            appointment=infant_appointment_2060,
            reason=SCHEDULED)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=NOT_REQUIRED,
            crf_entry__app_label='mb_infant',
            crf_entry__model_name='infantarvproph',
            appointment=infant_appointment_2060).count(), 1)

    def test_infant_arv_proph_required_till_discontinued_2(self):
        """Test if infant arv proph is not required if arv status of infant is discontinued"""
        registered_subject_infant = self.infant_arv_proph_setup()
        infant_appointment_2030 = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2030')
        infant_visit_2030 = InfantVisitFactory(
            appointment=infant_appointment_2030,
            reason=SCHEDULED)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=UNKEYED,
            crf_entry__app_label='mb_infant',
            crf_entry__model_name='infantarvproph',
            appointment=infant_appointment_2030).count(), 1)
        InfantArvProphFactory(infant_visit=infant_visit_2030, prophylatic_nvp=YES, arv_status=NO_MODIFICATIONS)
        infant_appointment_2060 = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2060')
        infant_visit_2060 = InfantVisitFactory(
            appointment=infant_appointment_2060,
            reason=SCHEDULED)
        InfantArvProphFactory(infant_visit=infant_visit_2060, prophylatic_nvp=YES, arv_status=DISCONTINUED)
        infant_appointment_2090 = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2090')
        InfantVisitFactory(
            appointment=infant_appointment_2090,
            reason=SCHEDULED)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=NOT_REQUIRED,
            crf_entry__app_label='mb_infant',
            crf_entry__model_name='infantarvproph',
            appointment=infant_appointment_2090).count(), 1)

    def test_infant_arv_proph_required_till_discontinued_3(self):
        """Test if infant arv proph is not required if arv status of infant is discontinued"""
        registered_subject_infant = self.infant_arv_proph_setup()
        infant_appointment_2030 = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2030')
        infant_visit_2030 = InfantVisitFactory(
            appointment=infant_appointment_2030,
            reason=SCHEDULED)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=UNKEYED,
            crf_entry__app_label='mb_infant',
            crf_entry__model_name='infantarvproph',
            appointment=infant_appointment_2030).count(), 1)
        InfantArvProphFactory(infant_visit=infant_visit_2030, prophylatic_nvp=YES, arv_status=DISCONTINUED)
        infant_appointment_2060 = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2060')
        InfantVisitFactory(
            appointment=infant_appointment_2060,
            reason=SCHEDULED)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=NOT_REQUIRED,
            crf_entry__app_label='mb_infant',
            crf_entry__model_name='infantarvproph',
            appointment=infant_appointment_2060).count(), 1)
        infant_appointment_2090 = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2090')
        InfantVisitFactory(
            appointment=infant_appointment_2090,
            reason=SCHEDULED)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=NOT_REQUIRED,
            crf_entry__app_label='mb_infant',
            crf_entry__model_name='infantarvproph',
            appointment=infant_appointment_2090).count(), 1)

    def infant_arv_proph_setup(self):
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES)
        self.assertEqual(postnatal_enrollment.enrollment_hiv_status, POS)
        maternal_appointment_1000M = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        MaternalVisitFactory(appointment=maternal_appointment_1000M)
        maternal_appointment_2000M = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='2000M')
        maternal_visit_2000 = MaternalVisitFactory(appointment=maternal_appointment_2000M)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit_2000)
        registered_subject_infant = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type=INFANT)
        InfantBirthFactory(
            registered_subject=registered_subject_infant,
            maternal_labour_del=maternal_labour_del)
        infant_appointment_2000 = Appointment.objects.get(
            visit_definition__code='2000',
            registered_subject=registered_subject_infant)
        InfantVisitFactory(appointment=infant_appointment_2000)
        infant_appointment_2010 = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2010')
        infant_visit_2010 = InfantVisitFactory(
            appointment=infant_appointment_2010,
            reason=SCHEDULED)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=UNKEYED,
            crf_entry__app_label='mb_infant',
            crf_entry__model_name='infantarvproph',
            appointment=infant_appointment_2010).count(), 1)
        InfantArvProphFactory(infant_visit=infant_visit_2010, prophylatic_nvp=YES, arv_status=NO_MODIFICATIONS)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=KEYED,
            crf_entry__app_label='mb_infant',
            crf_entry__model_name='infantarvproph',
            appointment=infant_appointment_2010).count(), 1)
        return registered_subject_infant
