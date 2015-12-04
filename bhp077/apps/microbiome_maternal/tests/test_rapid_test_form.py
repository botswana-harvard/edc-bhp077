from django.test import TestCase
from django.utils import timezone
from datetime import date

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc_constants.constants import YES, NO, POS, NEG

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_maternal.tests.factories import MaternalEligibilityFactory
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory
from bhp077.apps.microbiome_maternal.tests.factories import PostnatalEnrollmentFactory
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from bhp077.apps.microbiome_maternal.forms import RapidTestResultForm

from ..visit_schedule import AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule
from bhp077.apps.microbiome_maternal.tests.factories.maternal_visit_factory import MaternalVisitFactory


class TestRapidTestForm(TestCase):

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
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

        self.data = {
            'report_datetime': timezone.now(),
            'maternal_visit': None,
            'rapid_test_done': YES,
            'rapid_test_date': timezone.now(),
            'rapid_test_result': None,
        }

    def model_options(self, app_label, model_name, appointment):
        model_options = {}
        model_options.update(
            entry__app_label=app_label,
            entry__model_name=model_name,
            appointment=appointment)
        return model_options

    def test_validate_rapid_test_done_no_result(self):
        self.maternal_consent.dob = date(2015, 12, 7)
        self.maternal_consent.save()

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            verbal_hiv_status=NEG,
            evidence_hiv_status=YES,
        )
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M'
        )
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason='off study')

        self.data['maternal_visit'] = maternal_visit.id

        rapid_form = RapidTestResultForm(data=self.data)

        self.assertIn(u"If a rapid test was processed, what is the test result?", rapid_form.errors.get("__all__"))

    def test_validate_rapid_test_done_result(self):
        self.maternal_consent.dob = date(2015, 12, 7)
        self.maternal_consent.save()

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            verbal_hiv_status=NEG,
            evidence_hiv_status=YES,
        )
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M'
        )
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason='off study')

        self.data['maternal_visit'] = maternal_visit.id

        self.data['rapid_test_result'] = POS

        rapid_form = RapidTestResultForm(data=self.data)

        self.assertTrue(rapid_form.is_valid())

    def test_validate_rapid_test_done_no_rapid_test_date(self):
        self.maternal_consent.dob = date(2015, 12, 7)
        self.maternal_consent.save()

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            verbal_hiv_status=NEG,
            evidence_hiv_status=YES,
        )
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M'
        )
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason='scheduled')

        self.data['maternal_visit'] = maternal_visit.id

        self.data['rapid_test_date'] = None

        self.data['rapid_test_result'] = POS

        rapid_form = RapidTestResultForm(data=self.data)

        self.assertIn(u"If a rapid test was processed, what is the date of the rapid test?", rapid_form.errors.get("__all__"))

    def test_validate_rapid_test_done_processed(self):
        self.maternal_consent.dob = date(2015, 12, 7)
        self.maternal_consent.save()

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            verbal_hiv_status=NEG,
            evidence_hiv_status=YES,
        )
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M'
        )
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason='scheduled')

        self.data['maternal_visit'] = maternal_visit.id

        self.data['rapid_test_done'] = NO
        self.data['rapid_test_date'] = None
        self.data['rapid_test_result'] = None

        rapid_form = RapidTestResultForm(data=self.data)

        self.assertTrue(rapid_form.is_valid())

    def test_validate_rapid_test_done_processed1(self):
        self.maternal_consent.dob = date(2015, 12, 7)
        self.maternal_consent.save()

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            verbal_hiv_status=NEG,
            evidence_hiv_status=YES,
        )
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M'
        )
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason='scheduled')

        self.data['maternal_visit'] = maternal_visit.id

        self.data['rapid_test_done'] = NO
        self.data['rapid_test_date'] = timezone.now()
        self.data['rapid_test_result'] = None

        rapid_form = RapidTestResultForm(data=self.data)

        self.assertIn(u"If a rapid test was not processed, please do not provide rapid test date and result.", rapid_form.errors.get("__all__"))
