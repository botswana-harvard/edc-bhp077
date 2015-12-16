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
from microbiome.apps.mb_maternal.tests.factories import (
    MaternalEligibilityFactory, MaternalVisitFactory)
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory
from microbiome.apps.mb_list.models import Contraceptives

from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory
from microbiome.apps.mb_lab.lab_profiles import MaternalProfile
from microbiome.apps.mb_maternal.forms import MaternalSrhForm

from ..visit_schedule import AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule


class TestMaternalSrhForm(TestCase):

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

        maternal_eligibility = MaternalEligibilityFactory()
        maternal_consent = MaternalConsentFactory(
            registered_subject=maternal_eligibility.registered_subject)
        registered_subject = maternal_consent.registered_subject
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_date=date.today(),
            rapid_test_result=NEG)

        appointment1000 = Appointment.objects.get(
            registered_subject=postnatal_enrollment.registered_subject,
            visit_definition__code='1000M')
        appointment2000 = Appointment.objects.get(
            registered_subject=postnatal_enrollment.registered_subject,
            visit_definition__code='2000M')
        appointment2010 = Appointment.objects.get(
            registered_subject=postnatal_enrollment.registered_subject,
            visit_definition__code='2010M')

        MaternalVisitFactory(appointment=appointment1000, reason=SCHEDULED)
        MaternalVisitFactory(appointment=appointment2000, reason=SCHEDULED)
        maternal_visit = MaternalVisitFactory(appointment=appointment2010, reason=SCHEDULED)

        contraceptives = Contraceptives.objects.exclude(
            name__icontains='other').exclude(name__icontains=NOT_APPLICABLE).first()

        self.data = {
            'report_datetime': timezone.now(),
            'maternal_visit': maternal_visit.id,
            'seen_at_clinic': YES,
            'reason_unseen_clinic': None,
            'reason_unseen_clinic_other': None,
            'is_contraceptive_initiated': YES,
            'contr': [contraceptives.id],
            'contr_other': None,
            'reason_not_initiated': None,
            'srh_referral': YES,
            'srh_referral_other': None}

    def test_unseen_no_reason(self):
        """Test participant not seen at clinic but reason not provided"""
        self.data['seen_at_clinic'] = NO
        form = MaternalSrhForm(data=self.data)
        self.data['reason_unseen_clinic'] = None
        self.assertIn(
            'If you have not been seen in that clinic since your last visit with us, why not?',
            form.errors.get('__all__'))

    def test_srh_srh_form_valid3(self):
        """Asserts if have not initiated contraceptive methods raises."""
        self.data['seen_at_clinic'] = NO
        self.data['reason_unseen_clinic'] = 'not_sexually_active'
        self.data['is_contraceptive_initiated'] = NO
        contraceptives = Contraceptives.objects.exclude(name__icontains='other').first()
        self.data['contr'] = [contraceptives.id]
        form = MaternalSrhForm(data=self.data)
        self.assertIn(
            'If have not initiated contraceptive method, please provide reason.',
            form.errors.get('__all__') or [])

    def test_no_contraceptive_initiated_but_listed(self):
        """Test participant uses contraceptives but none listed"""
        self.data['is_contraceptive_initiated'] = NO
        form = MaternalSrhForm(data=self.data)
        self.assertIn(
            'If have not initiated contraceptive method, please provide reason.',
            form.errors.get('__all__'))

    def test_no_contraceptiove_reason_given(self):
        """Test not seen at clinic but reason unseen given"""
        self.data['seen_at_clinic'] = NO
        self.data['reason_not_initiated'] = "no_options"
        form = MaternalSrhForm(data=self.data)
        self.data['reason_unseen_clinic'] = 'not_sexually_active'
        self.assertIn(
            "Don't answer this question, since you have initiated contraceptive.",
            form.errors.get('__all__') or [])
