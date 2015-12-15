from django.test import TestCase
from django.utils import timezone

from edc.core.bhp_variables.tests.factories.study_site_factory import StudySiteFactory
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc_constants.choices import YES, POS, NOT_APPLICABLE

from microbiome.apps.mb.app_configuration.classes import MicrobiomeConfiguration
from microbiome.apps.mb_lab.lab_profiles import MaternalProfile
from microbiome.apps.mb_maternal.forms import MaternalHeightWeightForm
from microbiome.apps.mb_maternal.models import MaternalHeightWeight

from ..visit_schedule import PostnatalEnrollmentVisitSchedule
from .factories import (PostnatalEnrollmentFactory, MaternalVisitFactory,
                        MaternalEligibilityFactory, MaternalConsentFactory)


class BaseHeightTestModel(MaternalHeightWeight):
    class Meta:
        app_label = 'mb_maternal'


class BaseHeightForm(MaternalHeightWeightForm):

    class Meta:
        model = BaseHeightTestModel
        fields = '__all__'


class TestHeightWeight(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()
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
