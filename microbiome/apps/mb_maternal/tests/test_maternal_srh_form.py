from datetime import date
from django.test import TestCase
from django.utils import timezone

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc_constants.constants import YES, NO, NEG, SCHEDULED, NOT_APPLICABLE

from microbiome.apps.mb.app_configuration.classes import MicrobiomeConfiguration
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory, MaternalVisitFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory
from microbiome.apps.mb_list.models import Contraceptives

from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory
from microbiome.apps.mb_lab.lab_profiles import MaternalProfile
from microbiome.apps.mb_maternal.forms import MaternalSrhForm

from ..visit_schedule import AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule


class TestSrhServiceUtilizationForm(TestCase):

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
        contraceptives = Contraceptives.objects.exclude(
            name__icontains='other').exclude(name__icontains=NOT_APPLICABLE).first()
        self.data = {
            'report_datetime': timezone.now(),
            'maternal_visit': None,
            'seen_at_clinic': YES,
            'is_contraceptive_initiated': YES,
            'contr': [contraceptives.id],
            'contr_other': None,
            'reason_not_initiated': None,
            'srh_referral': YES,
            'srh_referral_other': None
        }

    def test_srh_srh_form_valid(self):
        """Asserts form data is valid from setup."""
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_date=date.today(),
            rapid_test_result=NEG)
        self.assertTrue(postnatal_enrollment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(
            appointment=appointment,
            reason=SCHEDULED)
        self.data['maternal_visit'] = maternal_visit.id
        form = MaternalSrhForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_srh_srh_form_valid2(self):
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_date=date.today(),
            rapid_test_result=NEG)
        self.assertTrue(postnatal_enrollment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(
            appointment=appointment,
            reason=SCHEDULED)
        self.data['seen_at_clinic'] = NO
        self.data['maternal_visit'] = maternal_visit.id
        form = MaternalSrhForm(data=self.data)
        self.data['reason_unseen_clinic'] = None
        self.assertIn(
            'If you have not been seen in that clinic since your last visit with us, why not?',
            form.errors.get('__all__'))

    def test_srh_srh_form_valid3(self):
        """Asserts if have not initiated contraceptive methods raises."""
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_date=date.today(),
            rapid_test_result=NEG)
        self.assertTrue(postnatal_enrollment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason=SCHEDULED)
        self.data['seen_at_clinic'] = NO
        self.data['reason_unseen_clinic'] = 'not_sexually_active'
        self.data['is_contraceptive_initiated'] = NO
        self.data['maternal_visit'] = maternal_visit.id
        contraceptives = Contraceptives.objects.exclude(name__icontains='other').first()
        self.data['contr'] = [contraceptives.id]
        form = MaternalSrhForm(data=self.data)
        self.assertIn(
            'If have not initiated contraceptive method, please provide reason.',
            form.errors.get('__all__') or [])

    def test_srh_srh_form_valid4(self):

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_date=date.today(),
            rapid_test_result=NEG)
        self.assertTrue(postnatal_enrollment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason=SCHEDULED)
        self.data['seen_at_clinic'] = NO
        self.data['reason_not_initiated'] = "no_options"
        self.data['maternal_visit'] = maternal_visit.id
        form = MaternalSrhForm(data=self.data)
        self.data['reason_unseen_clinic'] = 'not_sexually_active'
        self.assertIn(
            "Don't answer this question, since you have initiated contraceptive.",
            form.errors.get('__all__') or [])
