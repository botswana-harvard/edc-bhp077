from datetime import date
from django.utils import timezone

from edc_appointment.models import Appointment
from edc_constants.constants import YES, NO, NEG, SCHEDULED, NOT_APPLICABLE

from microbiome.apps.mb_maternal.tests.factories import (
    MaternalEligibilityFactory, MaternalVisitFactory)
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory
from microbiome.apps.mb_list.models import Contraceptives

from microbiome.apps.mb_maternal.forms import MaternalSrhForm

from .base_test_case import BaseTestCase
from .factories import PostnatalEnrollmentFactory


class TestMaternalSrhForm(BaseTestCase):

    def setUp(self):
        super(TestMaternalSrhForm, self).setUp()
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
            'If you have not initiated contraceptive method, please provide reason.',
            form.errors.get('__all__') or [])

    def test_no_contraceptive_initiated_but_listed(self):
        """Test participant uses contraceptives but none listed"""
        self.data['is_contraceptive_initiated'] = NO
        form = MaternalSrhForm(data=self.data)
        self.assertIn(
            'If you have not initiated contraceptive method, please provide reason.',
            form.errors.get('__all__'))

    def test_no_contraceptive_reason_given(self):
        """Test not seen at clinic but reason unseen given"""
        self.data['seen_at_clinic'] = NO
        self.data['reason_not_initiated'] = "no_options"
        form = MaternalSrhForm(data=self.data)
        self.data['reason_unseen_clinic'] = 'not_sexually_active'
        self.assertIn(
            "Don't answer this question, since you have initiated contraceptive.",
            form.errors.get('__all__') or [])

    def test_seen_at_clinic_dwta(self):
        """Test does not want to answer with reason unseen given"""
        self.data['seen_at_clinic'] = 'DWTA'
        self.data['reason_unseen_clinic'] = 'not_sexually_active'
        form = MaternalSrhForm(data=self.data)
        self.assertIn(
            'If participant does not want to answer, the questionnaire is complete.',
            form.errors.get('__all__'))

    def test_reason_unseen_clinic_not_tried(self):
        """Test not seen at clinic and reason unseen at clinic not tried"""
        self.data['seen_at_clinic'] = NO
        self.data['reason_unseen_clinic'] = 'not_tried'
        self.data['is_contraceptive_initiated'] = YES
        form = MaternalSrhForm(data=self.data)
        self.assertIn(
            'If participant answered I have not yet sought the clinic, the questionnaire is complete.',
            form.errors.get('__all__'))

    def test_init__no_contraceptive_given(self):
        """Test contraceptive initiated but no reason given"""
        self.data['seen_at_clinic'] = YES
        self.data['is_contraceptive_initiated'] = YES
        self.data['contr'] = None
        form = MaternalSrhForm(data=self.data)
        self.assertIn(
            'You indicated that contraceptives were initiated, please give a valid contraceptive.',
            form.errors.get('__all__') or [])

    def test_contraceptive_dwta(self):
        """Test test dont want to answer (DWTA) at contraceptive initiation"""
        self.data['seen_at_clinic'] = YES
        self.data['is_contraceptive_initiated'] = 'DWTA'
        form = MaternalSrhForm(data=self.data)
        self.assertIn(
            'Participant does not want to answer, the questionnaire is complete.',
            form.errors.get('__all__') or [])
