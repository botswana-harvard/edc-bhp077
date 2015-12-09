from django.test import TestCase
from django.utils import timezone

from edc.subject.registration.models import RegisteredSubject
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc_constants.constants import NEW, YES, NO, POS, NEG, NOT_REQUIRED

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome.constants import LIVE
from bhp077.apps.microbiome_infant.forms import InfantDeathForm
from bhp077.apps.microbiome_infant.models import InfantFu
from bhp077.apps.microbiome_infant.tests.factories import InfantBirthFactory, InfantVisitFactory
from bhp077.apps.microbiome_infant.visit_schedule import InfantBirthVisitSchedule
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile, InfantProfile
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from bhp077.apps.microbiome_maternal.tests.factories import MaternalEligibilityFactory, MaternalVisitFactory
from bhp077.apps.microbiome_maternal.tests.factories import PostnatalEnrollmentFactory
from bhp077.apps.microbiome_maternal.visit_schedule import PostnatalEnrollmentVisitSchedule


class TestInfantDeathForm(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
            site_lab_profiles.register(InfantProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()
        InfantBirthVisitSchedule().build()

        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_eligibility.registered_subject

        postnatal = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES)
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M')
        maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)
        infant_registered_subject = RegisteredSubject.objects.get(
            subject_type='infant', relative_identifier=self.registered_subject.subject_identifier)
        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2010')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)

        self.data = {
            'report_datetime': timezone.now(),
            'infant_visit': self.infant_visit.id,
            'death_date': timezone.now().date(),
            'death_cause_info': 'N/A',
            'death_cause_info_other': NO,
            'perform_autopsy': NO,
            'death_cause': NO,
            'death_cause_category': NO,
            'death_cause_other': None,
            'illness_duration': None,
            'death_medical_responsibility': None,
            'articipant_hospitalized': None,
            'death_reason_hospitalized': None,
            'participant_hospitalized': YES,
            'death_reason_hospitalized': None,
            'days_hospitalized': 0,
            'study_drug_relate': None,
            'infant_nvp_relate': None,
            'haart_relate': None,
            'trad_med_relate': None,
            'comment': None,
        }

    def test_infant_death_form_valid(self):
        infant_death_form = InfantDeathForm(data=self.data)
        print infant_death_form.errors
        self.assertTrue(infant_death_form.is_valid())

    def test_infant_validate_date_of_death(self):
        self.data['death_date'] = timezone.now().date()
        self.maternal_consent.consent_datetime = timezone.now()
        self.maternal_consent.save()
        infant_death_form = InfantDeathForm(data=self.data)
        self.assertIn(
            u'Consent_Datetime CANNOT be before consent datetime', infant_death_form.errors.get('__all__'))

    def test_death_reason_hospitalized_yes(self):
        self.data['participant_hospitalized'] = YES
        self.data['death_reason_hospitalized"'] = None
        infant_death_form = InfantDeathForm(data=self.data)
        self.assertIn(
            u'If the participant was hospitalized, what was the primary reason for hospitalisation?',
            infant_death_form.errors.get('__all__'))

    def test_death_reason_hospitalized_yes1(self):
        self.data['participant_hospitalized'] = YES
        self.data['death_reason_hospitalized"'] = None
        self.data['days_hospitalized'] = 0
        infant_death_form = InfantDeathForm(data=self.data)
        self.assertIn(
            u'If the participant was hospitalized, please provide number of days the participant was hospitalised.',
            infant_death_form.errors.get('__all__'))
