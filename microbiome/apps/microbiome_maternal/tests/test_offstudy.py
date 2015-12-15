from datetime import date
from django.test import TestCase
from django.utils import timezone

from edc.entry_meta_data.models import ScheduledEntryMetaData
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc_constants.constants import YES, POS, NEG, UNKEYED, OFF_STUDY, NOT_APPLICABLE

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome.constants import MIN_AGE_OF_CONSENT
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from bhp077.apps.microbiome_maternal.forms import MaternalOffStudyForm
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory
from bhp077.apps.microbiome_maternal.tests.factories import MaternalEligibilityFactory
from bhp077.apps.microbiome_maternal.tests.factories import PostnatalEnrollmentFactory, MaternalOffStudyFactory

from ..visit_schedule import AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule
from bhp077.apps.microbiome_maternal.tests.factories.maternal_visit_factory import MaternalVisitFactory
from dateutil.relativedelta import relativedelta


class TestOffStudy(TestCase):

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

        self.data = {
            'registered_subject': self.registered_subject.id,
            'reason': 'not_{}'.format(MIN_AGE_OF_CONSENT),
            'has_scheduled_data': YES,
            'maternal_visit': None,
            'offstudy_date': timezone.now().date()}

    def test_offstudy1(self):
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        MaternalVisitFactory(appointment=appointment, reason=OFF_STUDY)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(
            entry_status=UNKEYED,
            entry__app_label='microbiome_maternal',
            entry__model_name='maternaloffstudy',
            appointment=appointment).count(), 1)

    def test_offstudy2(self):
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(
            appointment=appointment,
            reason=OFF_STUDY)
        MaternalOffStudyFactory(
            registered_subject=appointment.registered_subject,
            report_datetime=timezone.now(),
            offstudy_date=date.today(),
            maternal_visit=maternal_visit)
        self.assertEqual(
            Appointment.objects.filter(
                registered_subject=self.registered_subject).count(), 1)

    def test_offstudy3(self):
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(
            appointment=appointment,
            report_datetime=timezone.now(),
            reason=OFF_STUDY)
        MaternalOffStudyFactory(
            registered_subject=appointment.registered_subject,
            maternal_visit=maternal_visit,
            report_datetime=timezone.now(),
            offstudy_date=date.today())
        self.assertEqual(Appointment.objects.filter(
            registered_subject=self.registered_subject).count(), 1)

    def test_validate_offstudy_date(self):
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(
            appointment=appointment,
            reason=OFF_STUDY)
        self.data['maternal_visit'] = maternal_visit.id
        self.data['offstudy_date'] = date(2015, 10, 6)
        offstudy_form = MaternalOffStudyForm(data=self.data)
        self.assertIn(
            "Off study date cannot be before consent date",
            offstudy_form.errors.get("__all__"))

    def test_validate_offstudy_date_consent_datetime(self):
        self.maternal_consent.consent_datetime = timezone.now() - relativedelta(weeks=1)
        self.maternal_consent.save()
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(
            appointment=appointment, reason=OFF_STUDY)
        self.data['maternal_visit'] = maternal_visit.id
        self.data['offstudy_date'] = timezone.now() - relativedelta(weeks=2)
        offstudy_form = MaternalOffStudyForm(data=self.data)
        self.assertIn(
            "Off study date cannot be before consent date",
            offstudy_form.errors.get("__all__"))
