from django.utils import timezone

from edc_appointment.models import Appointment
from edc_constants.choices import YES, NO, NOT_APPLICABLE, POS

from microbiome.apps.mb_list.models import ChronicConditions
from microbiome.apps.mb_maternal.forms import MaternalPostFuForm

from .base_maternal_test_case import BaseMaternalTestCase
from .factories import (PostnatalEnrollmentFactory, MaternalVisitFactory,
                        MaternalEligibilityFactory, MaternalConsentFactory)


class TestMaternalFollowup(BaseMaternalTestCase):
    """Test eligibility of a mother for postnatal followup."""

    def setUp(self):
        super(TestMaternalFollowup, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject,
            study_site=self.study_site)
        self.registered_subject = self.maternal_consent.registered_subject
        self.postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            will_breastfeed=YES
        )
        for code in ['1000M', '2000M']:
            appointment = Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code=code)
            MaternalVisitFactory(appointment=appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='2010M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        chronicition = ChronicConditions.objects.exclude(
            name__icontains='other').exclude(name__icontains=NOT_APPLICABLE).first()
        self.data = {
            'maternal_visit': self.maternal_visit.id,
            'report_datetime': timezone.now(),
            'weight_measured': NO,
            'weight_kg': '',
            'systolic_bp': 120,
            'diastolic_bp': 80,
            'chronic_since': NO,
            'chronic': [chronicition.id],
            'chronic_other': '',
            'comment': '',
        }

    def test_weight_1(self):
        """Assert that if mother indicated to be weighed, then weight cannot be empty"""
        self.data['weight_measured'] = YES
        form = MaternalPostFuForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You indicated that participant was weighed. Please provide the weight.',
                      errors)

    def test_weight_2(self):
        """Assert that if mother was not weighed CANNOT provide the weight."""
        self.data['weight_kg'] = 50
        form = MaternalPostFuForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You indicated that participant was NOT weighed, yet provided the weight. Please correct.',
                      errors)

    def test_weight_3(self):
        """Assert that if mother was not weighed and you dont provide the weight, form is valid."""
        form = MaternalPostFuForm(data=self.data)
        self.assertTrue(form.is_valid)

    def test_weight_4(self):
        """Assert that if mother was weighed, weight should be provided."""
        self.data['weight_measured'] = YES
        self.data['weight_kg'] = 50
        form = MaternalPostFuForm(data=self.data)
        self.assertTrue(form.is_valid)

    def test_chronic_1(self):
        """Assert that if has chronic conditions is indicated as YES, then chronic conditions cannot be N/A"""
        chronicition = ChronicConditions.objects.filter(name__icontains=NOT_APPLICABLE).first()
        self.data['chronic_since'] = YES
        self.data['chronic'] = [chronicition.id]
        form = MaternalPostFuForm(data=self.data)
        errors = ''.join(form.errors.get('__all__') or [])
        self.assertIn("You stated there ARE chronic conditionss, yet you selected 'N/A'", errors)

    def test_chronic_2(self):
        chronicition = ChronicConditions.objects.exclude(
            name__icontains='other').exclude(name__icontains=NOT_APPLICABLE).first()
        self.data['chronic_since'] = NO
        self.data['chronic'] = [chronicition.id]
        form = MaternalPostFuForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You stated there are NO chronic conditionss. Please correct', errors)

    def test_bp(self):
        self.data['chronic_since'] = NO
        self.data['chronic'] = None
        self.data['systolic_bp'] = 80
        self.data['diastolic_bp'] = 120
        form = MaternalPostFuForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Systolic blood pressure cannot be lower than the diastolic blood preassure', errors)
