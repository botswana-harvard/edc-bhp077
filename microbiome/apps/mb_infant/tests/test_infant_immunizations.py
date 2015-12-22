from django.test import TestCase
from django.utils import timezone
from datetime import date

from edc.subject.registration.models import RegisteredSubject
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc_appointment.models import Appointment
from edc_constants.constants import YES, NO, NEG

from microbiome.apps.mb.app_configuration.classes import MicrobiomeConfiguration
from microbiome.apps.mb.constants import INFANT
from microbiome.apps.mb_infant.forms import (
    InfantFuImmunizationsForm, VaccinesReceivedForm, VaccinesMissedForm)
from microbiome.apps.mb_infant.tests.factories import InfantBirthFactory, InfantVisitFactory
from microbiome.apps.mb_infant.visit_schedule import InfantBirthVisitSchedule
from microbiome.apps.mb_lab.lab_profiles import MaternalProfile, InfantProfile
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory, MaternalVisitFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory
from microbiome.apps.mb_maternal.visit_schedule import PostnatalEnrollmentVisitSchedule


class TestInfantImmunizations(TestCase):

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
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_eligibility.registered_subject
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M')
        maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)
        infant_registered_subject = RegisteredSubject.objects.get(
            subject_type=INFANT,
            relative_identifier=self.registered_subject.subject_identifier)
        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=maternal_labour_del)
        appointment1 = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        InfantVisitFactory(appointment=appointment1)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2010')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.data = {
            'report_datetime': timezone.now(),
            'infant_visit': self.infant_visit.id,
            'vaccines_received': YES,
            'vaccines_missed': NO
        }

    def test_vaccines_received_no_table_filling(self):
        """Test an infant who received vaccines but received vaccines table not filled"""
        form = InfantFuImmunizationsForm(data=self.data)
        self.assertIn("You mentioned that vaccines where received. Please"
                      " indicate which ones on the Received Vaccines table.",
                      form.errors.get('__all__'))

    def test_vaccines_missed_no_table_filling(self):
        """Test an infant who missed vaccines and missed vaccine table not filled"""
        self.data['vaccines_received'] = NO
        self.data['vaccines_missed'] = YES
        form = InfantFuImmunizationsForm(data=self.data)
        self.assertIn("You mentioned that the child missed some vaccines."
                      " Please indicate which ones in the Missed Vaccines "
                      "table.", form.errors.get('__all__'))

    def test_received_vaccine_fields(self):
        """Test that when a receive vaccine name is filled that a date is provided"""
        self.data['received_vaccine_name'] = 'BCG'
        self.data['date_given'] = ''
        self.data['infant_age'] = '2'
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("You provided a vaccine name {}. What date was it given to the "
                      "infant?".format(self.data['received_vaccine_name']), form.errors.get('__all__'))

    def test_missed_vaccine_fields(self):
        """Test that when a missed vaccine name is given that the reason should be provided"""
        self.data['missed_vaccine_name'] = 'BCG'
        self.data['reason_missed'] = ''
        form = VaccinesMissedForm(data=self.data)
        self.assertIn("You said {} vaccine was missed. Give a reason for missing this"
                      " vaccine".format(self.data['missed_vaccine_name']), form.errors.get('__all__'))

    def test_vaccination_at_birth(self):
        """Test that the correct vaccine is given at birth or few days after birth"""
        self.data['received_vaccine_name'] = 'BCG'
        self.data['infant_age'] = '2'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("BCG vaccination is ONLY given at birth or few days after birth",
                      form.errors.get('__all__'))

    def test_hepatitis_vaccine(self):
        """Test that the hepatitis vaccine is not given at inappropriate infant age"""
        self.data['received_vaccine_name'] = 'Hepatitis_B'
        self.data['infant_age'] = '6-11'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("Hepatitis B can only be administered at birth or 2 or 3 or 4 "
                      "months of infant life", form.errors.get('__all__'))

    def test_dpt_vaccine(self):
        """Test that DPT vaccine is not given at inappropriate infant age"""
        self.data['received_vaccine_name'] = 'DPT'
        self.data['infant_age'] = '6-11'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("DPT. Diphtheria, Pertussis and Tetanus can only be admistered at"
                      " 2 or 3 or 4 months ONLY.", form.errors.get('__all__'))

    def test_haemophilus_vaccine(self):
        """Test that haemophilus influenza vaccine is not administered at inappropiate infant age"""
        self.data['received_vaccine_name'] = 'Haemophilus_influenza'
        self.data['infant_age'] = '6-11'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("Haemophilus Influenza B vaccine can only be given at 2 or 3 or"
                      " 4 months of infant life.", form.errors.get('__all__'))

    def test_pcv_vaccine(self):
        """Test that PCV is administered at correct age"""
        self.data['received_vaccine_name'] = 'PCV_Vaccine'
        self.data['infant_age'] = '6-11'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("The PCV [Pneumonia Conjugated Vaccine], can ONLY be administered at"
                      " 2 or 3 or 4 months of infant life.", form.errors.get('__all__'))

    def test_polio_vaccine(self):
        """Test that polio vaccine is administered at correct age"""
        self.data['received_vaccine_name'] = 'Polio'
        self.data['infant_age'] = '6-11'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("Polio vaccine can only be administered at 2 or 3 or 4 or 18 "
                      "months of infant life", form.errors.get('__all__'))

    def test_rotavirus_vaccine(self):
        """Test rotavirus administered to infant at age 4months"""
        self.data['received_vaccine_name'] = 'Rotavirus'
        self.data['infant_age'] = '4'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("Rotavirus is only administered at 2 or 3 months of"
                      " infant life", form.errors.get('__all__'))

    def test_validate_measles_vaccine(self):
        """Test measles vaccine administered to an infant who is only a month old"""
        self.data['received_vaccine_name'] = 'Measles'
        self.data['infant_age'] = '2'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("Measles vaccine is only administered at 9 or 18"
                      " months of infant life.", form.errors.get('__all__'))

    def test_pentavalent_vaccine(self):
        """Test for Pentavalent vaccine administered at 6-11 months of infant life"""
        self.data['received_vaccine_name'] = 'Pentavalent'
        self.data['infant_age'] = '6-11'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("The Pentavalent vaccine can only be administered at 2 or 3 or"
                      " 4 months of infant life.", form.errors.get('__all__'))

    def test_validate_vitamin_a_vaccine(self):
        """Test for Vitamin A vaccine administered earlier than 6 months"""
        self.data['received_vaccine_name'] = 'Vitamin_A'
        self.data['infant_age'] = '2'
        self.data['date_given'] = date.today()
        form = VaccinesReceivedForm(data=self.data)
        self.assertIn("Vitamin A is given to children between 6-11 months of"
                      " life", form.errors.get('__all__'))
