from django.test import TestCase
from django.utils import timezone

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import site_rule_groups
from edc_constants.constants import YES, NEG, FEMALE

from microbiome.apps.mb.app_configuration.classes import MicrobiomeConfiguration
from microbiome.apps.mb_infant.forms import InfantBirthForm
from microbiome.apps.mb_infant.models import InfantBirth
from microbiome.apps.mb_infant.tests.factories import InfantBirthFactory
from microbiome.apps.mb_infant.visit_schedule import InfantBirthVisitSchedule
from microbiome.apps.mb_lab.lab_profiles import MaternalProfile, InfantProfile
from microbiome.apps.mb_maternal.tests.factories import (
    MaternalEligibilityFactory, MaternalVisitFactory, MaternalConsentFactory,
    PostnatalEnrollmentFactory, MaternalLabourDelFactory)
from microbiome.apps.mb_maternal.visit_schedule import PostnatalEnrollmentVisitSchedule


class TestInfantBirth(TestCase):

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

        maternal_eligibility = MaternalEligibilityFactory()
        maternal_consent = MaternalConsentFactory(registered_subject=maternal_eligibility.registered_subject)
        registered_subject = maternal_consent.registered_subject
        PostnatalEnrollmentFactory(
            registered_subject=registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)

        appointment1000 = Appointment.objects.get(
            registered_subject=registered_subject,
            visit_definition__code='1000M')
        appointment2000 = Appointment.objects.get(
            registered_subject=registered_subject,
            visit_definition__code='2000M')

        MaternalVisitFactory(appointment=appointment1000)
        maternal_visit = MaternalVisitFactory(appointment=appointment2000)
        self.maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)
        self.infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.maternal_labour_del.maternal_visit.appointment.registered_subject.subject_identifier,
            subject_type='infant')

        self.data = {
            'report_datetime': timezone.now(),
            'registered_subject': self.infant_registered_subject.id,
            'maternal_labour_del': self.maternal_labour_del.id,
            'first_name': 'FIRST NAME',
            'initials': 'FN',
            'dob': self.maternal_labour_del.delivery_datetime.date(),
            'gender': FEMALE}

    def test_infant_dob(self):
        """Test infant dob mismatching maternal labour delivery date"""
        self.data['registered_subject'] = self.infant_registered_subject.id
        self.data['dob'] = None
        form = InfantBirthForm(data=self.data)
        self.assertIn(
            'Infant dob must match maternal delivery date of {}. You wrote {}'.format(
                self.maternal_labour_del.delivery_datetime.date(), self.data['dob']),
            form.errors.get('__all__'))

    def test_saving_infant_birth(self):
        """Test resaving an already existing infant birth data form"""
        InfantBirthFactory(
            registered_subject=self.infant_registered_subject,
            maternal_labour_del=self.maternal_labour_del)
        form = InfantBirthForm(data=self.data)
        self.assertIn(
            'Infant birth record cannot be saved. An infant has already been registered'
            ' for this mother.',
            form.errors.get('__all__'))
