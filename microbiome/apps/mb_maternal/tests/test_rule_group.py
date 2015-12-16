from django.utils import timezone
from django.test import TestCase

from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc_constants.constants import NEW, YES, POS, NEG, UNKEYED, KEYED, NOT_REQUIRED, NOT_APPLICABLE

from microbiome.apps.mb.app_configuration.classes import MicrobiomeConfiguration
from microbiome.apps.mb_lab.lab_profiles import MaternalProfile
from microbiome.apps.mb_maternal.models import RapidTestResult
from microbiome.apps.mb_maternal.visit_schedule import (
    AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule)

from .factories import (
    MaternalEligibilityFactory, MaternalConsentFactory, MaternalVisitFactory,
    PostnatalEnrollmentFactory, ReproductiveHealthFactory, AntenatalEnrollmentFactory)


class TestRuleGroup(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        AntenatalEnrollmentVisitSchedule().build()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()

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
                self.assertEqual(ScheduledEntryMetaData.objects.filter(
                    entry_status=UNKEYED,
                    entry__app_label='mb_maternal',
                    entry__model_name=model_name,
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
                self.assertEqual(ScheduledEntryMetaData.objects.filter(
                    entry_status=UNKEYED,
                    entry__app_label='mb_maternal',
                    entry__model_name=model_name,
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
                self.assertEqual(ScheduledEntryMetaData.objects.filter(
                    entry_status=UNKEYED,
                    entry__app_label='mb_maternal',
                    entry__model_name=model_name,
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
                    self.assertEqual(ScheduledEntryMetaData.objects.filter(
                        entry_status=KEYED,
                        entry__app_label='mb_maternal',
                        entry__model_name=model_name,
                        appointment=appointment
                    ).count(), 1)
            else:
                for model_name in model_names:
                    self.assertEqual(ScheduledEntryMetaData.objects.filter(
                        entry_status=NOT_REQUIRED,
                        entry__app_label='mb_maternal',
                        entry__model_name=model_name,
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
                self.assertEqual(ScheduledEntryMetaData.objects.filter(
                    entry_status=UNKEYED,
                    entry__app_label='mb_maternal',
                    entry__model_name=model_name,
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
                registered_subject=self.registered_subject, visit_definition__code=code
            )
            ReproductiveHealthFactory(
                maternal_visit=MaternalVisitFactory(appointment=appointment)
            )
            self.assertEqual(ScheduledEntryMetaData.objects.filter(
                entry_status=NEW,
                app_label='mb_maternal',
                model_name='maternalsrh',
                appointment=appointment).count(), 1)
