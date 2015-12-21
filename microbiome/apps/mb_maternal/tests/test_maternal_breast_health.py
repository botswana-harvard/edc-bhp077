from django.utils import timezone

from edc.core.bhp_variables.tests.factories.study_site_factory import StudySiteFactory
from edc.subject.appointment.models import Appointment
from edc_constants.choices import YES, NO, POS, NOT_APPLICABLE

from microbiome.apps.mb_maternal.forms import (MaternalBreastHealthForm)

from .base_maternal_test_case import BaseMaternalTestCase
from .factories import (PostnatalEnrollmentFactory, MaternalVisitFactory,
                        MaternalEligibilityFactory, MaternalConsentFactory)


class TestMaternalBreastHealth(BaseMaternalTestCase):
    """Test eligibility of a mother for postnatal followup."""

    def setUp(self):
        super(TestMaternalBreastHealth, self).setUp()
        self.study_site = StudySiteFactory(site_code='10', site_name='Gabs')
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
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='2000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.data = {
            'maternal_visit': self.maternal_visit.id,
            'report_datetime': timezone.now(),
            'breast_feeding': NO,
            'has_mastitis': 'N/A',
            'mastitis': 'N/A',
            'has_lesions': 'N/A',
            'lesions': 'N/A',
            'advised_stop_bf': 'N/A',
            'why_not_advised': '',
        }

    def test_breastfeeding_1(self):
        """Assert that if mother has been breastfeeding, then expected to answer questions on mastitis"""
        self.data['breast_feeding'] = YES
        form = MaternalBreastHealthForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'You indicated that the mother has been breastfeeding. '
            'Has mastitis CANNOT be Not Applicable', errors)

    def test_breastfeeding_2(self):
        """Assert that if mother has been breastfeeding, then expected to answer questions on lesions"""
        self.data['breast_feeding'] = YES
        self.data['has_mastitis'] = NO
        form = MaternalBreastHealthForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            "You indicated that the mother has been breastfeeding. Has lesions CANNOT be Not Applicable",
            errors)

    def test_mastitis_1(self):
        """Assert that if mother has mastitis, then expected to indicate where"""
        self.data['breast_feeding'] = YES
        self.data['has_mastitis'] = YES
        self.data['has_lesions'] = NO
        form = MaternalBreastHealthForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You indicated the mother has mastitis. You cannot answer Not applicable'
                      ' to indicate where.', errors)

    def test_mastitis_2(self):
        """Assert that if mother does not have mastitis, then cannot indicate where"""
        self.data['breast_feeding'] = YES
        self.data['has_mastitis'] = NO
        self.data['mastitis'] = 'right breast'
        self.data['has_lesions'] = NO
        form = MaternalBreastHealthForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You stated that mother did not have mastitis, yet indicated '
                      'where mother if affected. Please correct.', errors)

    def test_lesions_1(self):
        """Assert that if mother has lesions, then expected to indicate where"""
        self.data['breast_feeding'] = YES
        self.data['has_mastitis'] = NO
        self.data['has_lesions'] = YES
        form = MaternalBreastHealthForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You stated that mother has lesions. Please indicate where.', errors)

    def test_lesions_2(self):
        """Assert that if mother does not have lesions, then cannot indicate where"""
        self.data['breast_feeding'] = YES
        self.data['has_mastitis'] = NO
        self.data['has_lesions'] = NO
        self.data['lesions'] = 'right breast'
        form = MaternalBreastHealthForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You stated that mother does not have lesions, yet indicated where she '
                      'has lesions. Please correct', errors)

    def test_advised_stop_bf_1(self):
        """Assert that if has_mastitis is YES then advised_stop_bf CANT be NOT_APPLICABLE"""
        self.data['breast_feeding'] = YES
        self.data['has_mastitis'] = YES
        self.data['has_lesions'] = NO
        self.data['mastitis'] = 'right breast'
        form = MaternalBreastHealthForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You indicated that participant has mastitis or has lesions. Was '
                      'participant advised to stop breast feeding CANNOT be Not Applicable.', errors)

    def test_advised_stop_bf_2(self):
        """Assert that if has_lesions is YES then advised_stop_bf CANT be NOT_APPLICABLE"""
        self.data['breast_feeding'] = YES
        self.data['has_mastitis'] = NO
        self.data['has_lesions'] = YES
        self.data['lesions'] = 'right breast'
        form = MaternalBreastHealthForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You indicated that participant has mastitis or has lesions. Was '
                      'participant advised to stop breast feeding CANNOT be Not Applicable.', errors)

    def test_advised_stop_bf_3(self):
        """Assert that if mother has not been breast-feeding then advised_stop_bf CANT be YES"""
        self.data['breast_feeding'] = NO
        self.data['advised_stop_bf'] = YES
        form = MaternalBreastHealthForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You indicated that the mother has not been breast feeding, question on whether'
                      ' she was advised to stop breast feeding should be Not Applicable.', errors)

    def test_advised_stop_bf_4(self):
        """Assert that if mother has not been breast-feeding then advised_stop_bf CANT be YES"""
        self.data['breast_feeding'] = YES
        self.data['has_mastitis'] = NO
        self.data['has_lesions'] = NO
        self.data['advised_stop_bf'] = NOT_APPLICABLE
        form = MaternalBreastHealthForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You indicated that the mother has been breast feeding, question on '
                      'whether she was advised to stop breast feeding CANNOT be Not Applicable.', errors)
