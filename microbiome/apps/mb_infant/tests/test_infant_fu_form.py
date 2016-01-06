from django.test import TestCase
from django.utils import timezone

from edc_registration.models import RegisteredSubject
from edc_lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc_rule_groups.classes import site_rule_groups
from edc_lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc_appointment.models import Appointment
from edc_constants.constants import YES, NO, NEG

from microbiome.apps.mb.app_configuration import AppConfiguration
from microbiome.apps.mb.constants import INFANT
from microbiome.apps.mb_infant.forms import InfantFuForm
from microbiome.apps.mb_infant.models import InfantFu
from microbiome.apps.mb_infant.tests.factories import InfantBirthFactory, InfantVisitFactory
from microbiome.apps.mb_infant.visit_schedule import InfantBirthVisitSchedule
from microbiome.apps.mb_lab.lab_profiles import MaternalProfile, InfantProfile
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory, MaternalVisitFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory
from microbiome.apps.mb_maternal.visit_schedule import PostnatalEnrollmentVisitSchedule


class BaseTestInfantFuModel(InfantFu):
    class Meta:
        app_label = 'mb_infant'


class BaseTestInfantFuForm(InfantFuForm):

    class Meta:
        model = BaseTestInfantFuModel
        fields = '__all__'


class TestInfantFu(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
            site_lab_profiles.register(InfantProfile())
        except AlreadyRegisteredLabProfile:
            pass
        AppConfiguration(lab_profiles=site_lab_profiles).prepare()
        site_lab_tracker.autodiscover()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()
        InfantBirthVisitSchedule().build()

        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_eligibility.registered_subject

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M')
        maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)
        infant_registered_subject = RegisteredSubject.objects.get(
            subject_type=INFANT, relative_identifier=self.registered_subject.subject_identifier)
        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2010')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.data = {
            'report_datetime': timezone.now(),
            'infant_birth': self.infant_birth.id,
            'infant_visit': self.infant_visit.id,
            'physical_assessment': NO,
            'diarrhea_illness': NO,
            'has_dx': NO,
            'was_hospitalized': NO,
        }

    def test_infant_hospitalization(self):
        self.data['infant_birth'] = self.infant_visit.id
        self.data['was_hospitalized'] = YES
        infant_fu = BaseTestInfantFuForm(data=self.data)
        self.assertIn(
            'If infant was hospitalized, please provide # of days hospitalized',
            infant_fu.errors.get('__all__'))

    def test_validate_hospitalization_duration(self):
        self.data['infant_birth'] = self.infant_visit.id
        self.data['was_hospitalized'] = YES
        self.data['days_hospitalized'] = 100
        infant_fu = BaseTestInfantFuForm(data=self.data)
        self.assertIn(
            'days hospitalized cannot be greater than 90days',
            infant_fu.errors.get('__all__'))
