from django.utils import timezone

from edc_appointment.models import Appointment
from edc_constants.constants import (NEW, YES, POS, NEG, UNKEYED, KEYED, REQUIRED, NOT_REQUIRED, NOT_APPLICABLE, NO)
from edc_meta_data.models import CrfMetaData, RequisitionMetaData

from microbiome.apps.mb_maternal.models import RapidTestResult

from ..models import MaternalClinicalHistory

from .base_test_case import BaseTestCase
from .factories import (
    MaternalEligibilityFactory, MaternalConsentFactory, MaternalVisitFactory,
    PostnatalEnrollmentFactory, ReproductiveHealthFactory, AntenatalEnrollmentFactory)


class TestRuleGroup(BaseTestCase):

    def setUp(self):
        super(TestRuleGroup, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

    def test_postnatal_enrollment_hiv_status(self):
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            will_breastfeed=YES,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            valid_regimen=YES)
        visit_codes = [['1000M', ['maternalclinicalhistory', 'maternalarvhistory', 'maternalarvpreg']]]
        for visit in visit_codes:
            code, model_names = visit
            appointment = Appointment.objects.get(
                registered_subject=self.registered_subject, visit_definition__code=code)
            MaternalVisitFactory(appointment=appointment)
            for model_name in model_names:
                self.assertEqual(CrfMetaData.objects.filter(
                    entry_status=UNKEYED,
                    crf_entry__app_label='mb_maternal',
                    crf_entry__model_name=model_name,
                    appointment=appointment
                ).count(), 1)

    def test_antenatal_enrollment_hiv_status(self):
        AntenatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            will_breastfeed=YES,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            valid_regimen=YES)
        visit_codes = [['1000M', ['maternalclinicalhistory', 'maternalarvhistory', 'maternalarvpreg']]]
        for visit in visit_codes:
            code, model_names = visit
            appointment = Appointment.objects.get(
                registered_subject=self.registered_subject, visit_definition__code=code)
            MaternalVisitFactory(appointment=appointment)
            for model_name in model_names:
                self.assertEqual(CrfMetaData.objects.filter(
                    entry_status=UNKEYED,
                    crf_entry__app_label='mb_maternal',
                    crf_entry__model_name=model_name,
                    appointment=appointment
                ).count(), 1)

    def test_hiv_rapid_test_neg(self):

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M')
        MaternalVisitFactory(appointment=appointment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M')
        MaternalVisitFactory(appointment=appointment)
        visit_codes = [
            ['2010M', ['rapidtestresult']],
            ['2030M', ['rapidtestresult']],
            ['2060M', ['rapidtestresult']],
            ['2090M', ['rapidtestresult']],
            ['2120M', ['rapidtestresult']]
        ]
        for visit in visit_codes:
            code, model_names = visit
            appointment = Appointment.objects.get(
                registered_subject=self.registered_subject, visit_definition__code=code)
            MaternalVisitFactory(appointment=appointment)
            for model_name in model_names:
                self.assertEqual(CrfMetaData.objects.filter(
                    entry_status=UNKEYED,
                    crf_entry__app_label='mb_maternal',
                    crf_entry__model_name=model_name,
                    appointment=appointment
                ).count(), 1)

    def test_hiv_rapid_test_keyed_pos(self):
        """ Sero Converter neg to pos, rapidtestresult is not required."""
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M')
        MaternalVisitFactory(appointment=appointment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M')
        MaternalVisitFactory(appointment=appointment)
        visit_codes = [
            ['2010M', ['rapidtestresult']],
            ['2030M', ['rapidtestresult']],
        ]
        for visit in visit_codes:
            code, model_names = visit
            appointment = Appointment.objects.get(
                registered_subject=self.registered_subject, visit_definition__code=code)
            maternal_visit = MaternalVisitFactory(appointment=appointment)
            if code == '2010M':
                RapidTestResult.objects.create(
                    report_datetime=timezone.now(),
                    maternal_visit=maternal_visit,
                    rapid_test_done=YES,
                    result_date=timezone.now().date(),
                    result=POS)
                for model_name in model_names:
                    self.assertEqual(CrfMetaData.objects.filter(
                        entry_status=KEYED,
                        crf_entry__app_label='mb_maternal',
                        crf_entry__model_name=model_name,
                        appointment=appointment
                    ).count(), 1)
            else:
                for model_name in model_names:
                    self.assertEqual(CrfMetaData.objects.filter(
                        entry_status=NOT_REQUIRED,
                        crf_entry__app_label='mb_maternal',
                        crf_entry__model_name=model_name,
                        appointment=appointment
                    ).count(), 1)

    def test_enrollment_hiv_status_neg(self):

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M')
        MaternalVisitFactory(appointment=appointment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M')
        MaternalVisitFactory(appointment=appointment)
        visit_codes = [
            ['2010M', ['rapidtestresult']],
            ['2030M', ['rapidtestresult']],
            ['2060M', ['rapidtestresult']],
            ['2090M', ['rapidtestresult']],
            ['2120M', ['rapidtestresult']]
        ]
        for visit in visit_codes:
            code, model_names = visit
            appointment = Appointment.objects.get(
                registered_subject=self.registered_subject, visit_definition__code=code)
            MaternalVisitFactory(appointment=appointment)
            for model_name in model_names:
                self.assertEqual(CrfMetaData.objects.filter(
                    entry_status=UNKEYED,
                    crf_entry__app_label='mb_maternal',
                    crf_entry__model_name=model_name,
                    appointment=appointment
                ).count(), 1)

    def test_hiv_pos_vl(self):

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M')
        MaternalVisitFactory(appointment=appointment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M')
        MaternalVisitFactory(appointment=appointment)
        visit_codes = [
            ['2010M', ['maternalrequisition']],
            ['2030M', ['maternalrequisition']],
            ['2060M', ['maternalrequisition']],
            ['2090M', ['maternalrequisition']],
            ['2120M', ['maternalrequisition']]
        ]
        for visit in visit_codes:
            code, model_names = visit
            appointment = Appointment.objects.get(
                registered_subject=self.registered_subject, visit_definition__code=code
            )
            MaternalVisitFactory(appointment=appointment)
            for model_name in model_names:
                self.assertEqual(
                    RequisitionMetaData.objects.filter(
                        entry_status=NEW,
                        lab_entry__app_label='mb_lab',
                        lab_entry__model_name=model_name,
                        lab_entry__requisition_panel__name='Viral Load',
                        appointment=appointment).count(), 1)

    def test_breastmilk_for_pos_at_2010M(self):
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M')
        MaternalVisitFactory(appointment=appointment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M')
        MaternalVisitFactory(appointment=appointment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2010M')
        MaternalVisitFactory(appointment=appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(
            entry_status=NEW,
            lab_entry__app_label='mb_lab',
            lab_entry__model_name='maternalrequisition',
            lab_entry__requisition_panel__name='Breast Milk (Storage)',
            appointment=appointment).count(), 1)

    def test_srh_referral_yes_on_srh(self):
        """
        """
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            rapid_test_done=YES,
            will_breastfeed=YES,
            rapid_test_result=POS)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M')
        MaternalVisitFactory(appointment=appointment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M')
        MaternalVisitFactory(appointment=appointment)
        for code in ['2010M', '2030M']:
            appointment = Appointment.objects.get(
                registered_subject=self.registered_subject, visit_definition__code=code)
            ReproductiveHealthFactory(
                maternal_visit=MaternalVisitFactory(appointment=appointment))
            self.assertEqual(CrfMetaData.objects.filter(
                entry_status=NEW,
                crf_entry__app_label='mb_maternal',
                crf_entry__model_name='maternalsrh',
                appointment=appointment).count(), 1)

    def test_maternal_arv_history_1(self):
        """Maternal ARV history should be required if prior_health_haart is answered as YES"""
        self.postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            will_breastfeed=YES
        )
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        MaternalClinicalHistory.objects.create(
            maternal_visit=self.maternal_visit,
            prev_preg_azt=YES,
            prev_sdnvp_labour=NO,
            prev_preg_haart=YES,
            lowest_cd4_known=NO,
            prior_health_haart=YES,
            prev_pregnancy_arv=NO,
            know_hiv_status='Nobody',
        )
        meta = CrfMetaData.objects.get(
            crf_entry__app_label='mb_maternal',
            crf_entry__model_name='maternalarvhistory',
            appointment=self.appointment)
        self.assertEqual(meta.entry_status, REQUIRED)

    def test_maternal_arv_history_2(self):
        """Maternal ARV history should be required if evidence_hiv_status is answered as YES"""
        self.postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            will_breastfeed=YES
        )
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        MaternalClinicalHistory.objects.create(
            maternal_visit=self.maternal_visit,
            prev_preg_azt=YES,
            prev_sdnvp_labour=NO,
            prev_preg_haart=YES,
            lowest_cd4_known=NO,
            prior_health_haart=NO,
            prev_pregnancy_arv=YES,
            know_hiv_status='Nobody',
        )
        meta = CrfMetaData.objects.get(
            crf_entry__app_label='mb_maternal',
            crf_entry__model_name='maternalarvhistory',
            appointment=self.appointment)
        self.assertEqual(meta.entry_status, REQUIRED)

    def test_maternal_arv_history_3(self):
        """Maternal ARV history should be required if evidence_hiv_status and prior_health_haart is answered as YES"""
        self.postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            will_breastfeed=YES
        )
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        MaternalClinicalHistory.objects.create(
            maternal_visit=self.maternal_visit,
            prev_preg_azt=YES,
            prev_sdnvp_labour=NO,
            prev_preg_haart=YES,
            lowest_cd4_known=NO,
            prior_health_haart=YES,
            prev_pregnancy_arv=YES,
            know_hiv_status='Nobody',
        )
        meta = CrfMetaData.objects.get(
            crf_entry__app_label='mb_maternal',
            crf_entry__model_name='maternalarvhistory',
            appointment=self.appointment)
        self.assertEqual(meta.entry_status, REQUIRED)

    def test_maternal_arv_history_4(self):
        """Maternal ARV history should NOT be required if evidence_hiv_status and
        prior_health_haart is answered as NO"""
        self.postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            will_breastfeed=YES
        )
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        MaternalClinicalHistory.objects.create(
            maternal_visit=self.maternal_visit,
            prev_preg_azt=YES,
            prev_sdnvp_labour=NO,
            prev_preg_haart=YES,
            lowest_cd4_known=NO,
            prior_health_haart=NO,
            prev_pregnancy_arv=NO,
            know_hiv_status='Nobody',
        )
        meta = CrfMetaData.objects.get(
            crf_entry__app_label='mb_maternal',
            crf_entry__model_name='maternalarvhistory',
            appointment=self.appointment)
        self.assertEqual(meta.entry_status, NOT_REQUIRED)
