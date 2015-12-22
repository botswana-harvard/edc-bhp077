from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import date, datetime

from edc.core.bhp_variables.tests.factories.study_site_factory import StudySiteFactory
from edc_appointment.models import Appointment
from edc_constants.choices import YES, NO, POS, NOT_APPLICABLE
from edc_constants.constants import CONTINUOUS, STOPPED, RESTARTED

from microbiome.apps.mb_list.models import PriorArv
from microbiome.apps.mb_maternal.forms import (MaternalArvHistoryForm)

from .base_maternal_test_case import BaseMaternalTestCase
from .factories import (PostnatalEnrollmentFactory, MaternalVisitFactory,
                        MaternalEligibilityFactory, MaternalConsentFactory)


class TestMaternalArvHistory(BaseMaternalTestCase):
    """Test eligibility of a mother for postnatal followup."""

    def setUp(self):
        super(TestMaternalArvHistory, self).setUp()
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
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        prior_arv = PriorArv.objects.exclude(
            name__icontains='other').exclude(name__icontains=NOT_APPLICABLE).first()
        self.data = {
            'maternal_visit': self.maternal_visit.id,
            'report_datetime': timezone.now(),
            'haart_start_date': date.today() - relativedelta(weeks=7),
            'is_date_estimated': '-',
            'preg_on_haart': YES,
            'haart_changes': 0,
            'prior_preg': CONTINUOUS,
            'prior_arv': [prior_arv.id],
        }

    def test_arv_interrupt_1(self):
        """Assert that if was not still on ARV then 'interruption never restarted'
        is not a valid option."""

        self.data['prior_preg'] = STOPPED
        self.data['haart_start_date'] = date(2015, 04, 10)
        self.data['preg_on_haart'] = YES
        form = MaternalArvHistoryForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn("You indicated that the mother was still on triple ARV when "
                      "she got pregnant, yet you indicated that ARVs were interrupted "
                      "and never restarted.", errors)

    def test_arv_interrupt_2(self):
        """Assert that if was not on ARV then 'Had treatment
        interruption but restarted' is not a valid option."""
        self.data['preg_on_haart'] = NO
        self.data['prior_preg'] = RESTARTED
        form = MaternalArvHistoryForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'You indicated that the mother was NOT on triple ARV when she got pregnant. '
            'ARVs could not have been interrupted. Please correct.', errors)

    def test_arv_interrupt_3(self):
        """Assert that if was not still on ARV then 'Received continuous HAART from the
        time she started is not a valid option."""
        self.data['preg_on_haart'] = NO
        self.data['prior_preg'] = CONTINUOUS
        form = MaternalArvHistoryForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'You indicated that the mother was NOT on triple ARV when she got pregnant. '
            'ARVs could not have been uninterrupted. Please correct.', errors)

    def test_arv_interrupt_4(self):
        """Assert that if was not still on ARV only valid answer is 'interrupted and never
        restarted'"""
        self.data['preg_on_haart'] = NO
        self.data['prior_preg'] = STOPPED
        form = MaternalArvHistoryForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_haart_start_date(self):
        """ARV start date should be six weeks prior to today"""
        self.data['haart_start_date'] = timezone.now()
        form = MaternalArvHistoryForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn("ARV start date must be six weeks prior to today's date or greater.", errors)

    def test_haart_start_date_2(self):
        """Start date of ARVs CANNOT be before DOB"""
        self.data['haart_start_date'] = date(1987, 10, 10)
        self.data['report_datetime'] = datetime.today()
        form = MaternalArvHistoryForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn("Date of triple ARVs first started CANNOT be before DOB.", errors)
