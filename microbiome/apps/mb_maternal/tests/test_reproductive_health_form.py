from datetime import date
from django.utils import timezone

from edc_appointment.models import Appointment
from edc_constants.constants import YES, NO, NEG, SCHEDULED, NOT_APPLICABLE

from microbiome.apps.mb_maternal.tests.factories import (
    MaternalEligibilityFactory, MaternalVisitFactory)
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory
from microbiome.apps.mb_list.models import Contraceptives, MaternalRelatives

from microbiome.apps.mb_maternal.forms import ReproductiveHealthForm

from .base_test_case import BaseTestCase
from .factories import PostnatalEnrollmentFactory


class TestReproductiveHealthForm(BaseTestCase):

    def setUp(self):
        super(TestReproductiveHealthForm, self).setUp()
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

        maternal_relatives = MaternalRelatives.objects.exclude(
            name__icontains='other').exclude(name__icontains=NOT_APPLICABLE).first()

        self.data = {
            'report_datetime': timezone.now(),
            'maternal_visit': maternal_visit.id,
            'more_children': YES,
            'next_child': 'between 2-5years from now',
            'contraceptive_measure': YES,
            'contraceptive_partner': YES,
            'contraceptive_relative': [maternal_relatives.id],
            'influential_decision_making': 'partner_most_influential',
            'uses_contraceptive': YES,
            'contr': [contraceptives.id],
            'pap_smear': YES,
            'pap_smear_date': date.today(),
            'pap_smear_estimate': NO,
            'pap_smear_result': YES,
            'pap_smear_result_status': 'normal',
            'pap_smear_result_abnormal': None,
            'srh_referral': YES}

    def test_more_children(self):
        self.data['more_children'] = NO
        self.data['next_child'] = 'between 2-5years from now'
        form = ReproductiveHealthForm(data=self.data)
        self.assertIn(
            'You said the client does not desire more children please do not answer '
            'When would you like to have your next child?',
            form.errors.get('__all__'))

    def test_next_none(self):
        self.data['more_children'] = YES
        self.data['next_child'] = None
        self.data['contraceptive_measure'] = YES
        form = ReproductiveHealthForm(data=self.data)
        self.assertIn(
            'Participant desires more children, question on next child cannot be None.',
            form.errors.get('__all__'))

    def test_uses_contraceptive_yes(self):
        self.data['more_children'] = YES
        self.data['uses_contraceptive'] = YES
        self.data['contr'] = None
        form = ReproductiveHealthForm(data=self.data)
        self.assertIn(
            'Participant uses a contraceptive method, please select a valid method',
            form.errors.get('__all__'))

    def test_uses_contraceptive_no(self):
        self.data['more_children'] = YES
        self.data['uses_contraceptive'] = NO
        form = ReproductiveHealthForm(data=self.data)
        self.assertIn(
            'Participant does not use a contraceptive method, no need to give a contraceptive method',
            form.errors.get('__all__'))

    def test_pap_smear_yes(self):
        self.data['pap_smear'] = YES
        self.data['pap_smear_date'] = None
        form = ReproductiveHealthForm(data=self.data)
        self.assertIn('Please give the date the pap smear was done.', form.errors.get('__all__'))

    def test_pap_smear_no(self):
        self.data['pap_smear'] = NO
        self.data['pap_smear_date'] = date.today()
        form = ReproductiveHealthForm(data=self.data)
        self.assertIn(
            'Pap smear date not known, please do not add it.',
            form.errors.get('__all__'))

    def test_pap_smear_result_yes(self):
        self.data['pap_smear'] = YES
        self.data['pap_smear_date'] = date.today()
        self.data['pap_smear_result'] = YES
        self.data['pap_smear_result_status'] = None
        form = ReproductiveHealthForm(data=self.data)
        self.assertIn(
            'Participant knows her pap smear result, please give the status of the pap smear.',
            form.errors.get('__all__'))

    def test_pap_smear_result_no(self):
        self.data['pap_smear'] = YES
        self.data['pap_smear_date'] = date.today()
        self.data['pap_smear_result'] = NO
        self.data['pap_smear_result_status'] = 'abnormal'
        self.data['pap_smear_result_abnormal'] = 'Yeast Infection'
        form = ReproductiveHealthForm(data=self.data)
        self.assertIn(
            'Participant pap smear result not known, no need to give pap smear status or notification date.',
            form.errors.get('__all__'))

    def test_pap_smear_date_estimate(self):
        self.data['pap_smear'] = YES
        self.data['pap_smear_date'] = date.today()
        self.data['pap_smear_estimate'] = None
        form = ReproductiveHealthForm(data=self.data)
        self.assertIn(
            'Pap smear date has been provided, please let us know if this date has been estimated.',
            form.errors.get('__all__'))
