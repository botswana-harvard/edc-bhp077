from django.utils import timezone

from edc_appointment.models import Appointment
from edc_constants.choices import YES, POS, NOT_APPLICABLE

from microbiome.apps.mb_maternal.forms import MaternalHeightWeightForm
from microbiome.apps.mb_maternal.models import MaternalHeightWeight

from .factories import (PostnatalEnrollmentFactory, MaternalVisitFactory,
                        MaternalEligibilityFactory, MaternalConsentFactory)

from .base_maternal_test_case import BaseMaternalTestCase


class BaseHeightTestModel(MaternalHeightWeight):
    class Meta:
        app_label = 'mb_maternal'


class BaseHeightForm(MaternalHeightWeightForm):

    class Meta:
        model = BaseHeightTestModel
        fields = '__all__'


class TestHeightWeight(BaseMaternalTestCase):

    def setUp(self):
        super(TestHeightWeight, self).setUp()
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
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.data = {
            'maternal_visit': self.maternal_visit.id,
            'report_datetime': timezone.now(),
            'weight_kg': 50.0,
            'height': 160.0,
            'systolic_bp': 120,
            'diastolic_bp': 80,
        }

    def test_bp(self):
        self.data['systolic_bp'] = 60
        self.data['diastolic_bp'] = 80
        form = BaseHeightForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn("Systolic blood pressure cannot be lower than the diastolic blood pressure.", errors)
