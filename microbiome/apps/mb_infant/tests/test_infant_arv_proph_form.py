from django.utils import timezone
from datetime import date

from edc_registration.models import RegisteredSubject
from edc_appointment.models import Appointment
from edc_constants.constants import YES, POS, NO, UNKNOWN

from microbiome.apps.mb.constants import INFANT, NO_MODIFICATIONS, MODIFIED, DISCONTINUED
from microbiome.apps.mb_infant.forms import (InfantArvProphForm, InfantArvProphModForm)
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory, MaternalVisitFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory

from microbiome.apps.mb_infant.tests.factories import (
    InfantBirthFactory, InfantVisitFactory, InfantArvProphFactory, InfantBirthArvFactory)

from ...mb.constants import NEVER_STARTED
from .base_test_case import BaseTestCase


class TestInfantArvProph(BaseTestCase):

    def setUp(self):
        super(TestInfantArvProph, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES)
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
        self.infant_birth_arv = InfantBirthArvFactory(infant_visit=self.infant_visit, azt_discharge_supply=YES)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2010')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.data = {
            'report_datetime': timezone.now(),
            'infant_visit': self.infant_visit.id,
            'prophylatic_nvp': YES,
            'arv_status': 'modified',
        }

    def test_validate_taking_arv_proph_no(self):
        """Test if the infant was not taking prophylactic arv and arv status is not Not Applicable"""
        self.data['prophylatic_nvp'] = NO
        self.data['arv_status'] = MODIFIED
        infant_arv_proph = InfantArvProphForm(data=self.data)
        self.assertIn(u'Infant was not taking prophylactic arv, prophylaxis should be Never Started or Discontinued.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_taking_arv_proph_discontinued(self):
        """Test if the was not taking  prophylactic arv and infant was not given arv's at birth"""
        self.infant_birth_arv.azt_discharge_supply = UNKNOWN
        self.infant_birth_arv.save()
        self.data['prophylatic_nvp'] = NO
        self.data['arv_status'] = DISCONTINUED
        infant_arv_proph = InfantArvProphForm(data=self.data)
        self.assertIn(
            u'The azt discharge supply in Infant birth arv was answered as NO or Unknown, '
            'therefore Infant ARV proph in this visit cannot be permanently discontinued.',
            infant_arv_proph.errors.get('__all__'))

    def test_validate_taking_arv_proph_yes(self):
        """Test if the infant was not taking prophylactic arv and arv status is Never Started"""
        self.data['prophylatic_nvp'] = YES
        self.data['arv_status'] = NEVER_STARTED
        infant_arv_proph = InfantArvProphForm(data=self.data)
        self.assertIn(u'Infant has been on prophylactic arv, cannot choose Never Started or Permanently discontinued.',
                      infant_arv_proph.errors.get('__all__'))

#     def test_validate_infant_arv_proph_mod(self):
#         """Test if the infant arv status was modified but no Arv Code given on inline."""
#         self.data['prophylatic_nvp'] = YES
#         self.data['arv_status'] = MODIFIED
#         infant_arv_proph = InfantArvProphForm(data=self.data)
#         self.assertIn(u'You indicated that the infant arv was modified, please give a valid Arv Code',
#                       infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_dose_status(self):
        proph = InfantArvProphFactory(infant_visit=self.infant_visit, arv_status=MODIFIED)
        inline_data = {'infant_arv_proph': proph.id,
                       'arv_code': 'Nevirapine',
                       'dose_status': None,
                       'modification_date': date.today(),
                       'modification_code': 'Initial dose'}
        infant_arv_proph = InfantArvProphModForm(data=inline_data)
        self.assertIn(u'You entered an ARV Code, please give the dose status.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_date(self):
        proph = InfantArvProphFactory(infant_visit=self.infant_visit, arv_status=MODIFIED)
        inline_data = {'infant_arv_proph': proph.id,
                       'arv_code': 'Nevirapine',
                       'dose_status': 'New',
                       'modification_date': None,
                       'modification_code': 'Initial dose'}
        infant_arv_proph = InfantArvProphModForm(data=inline_data)
        self.assertIn(u'You entered an ARV Code, please give the modification date.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_code(self):
        proph = InfantArvProphFactory(infant_visit=self.infant_visit, arv_status=MODIFIED)
        inline_data = {'infant_arv_proph': proph.id,
                       'arv_code': 'Nevirapine',
                       'dose_status': 'New',
                       'modification_date': date.today(),
                       'modification_code': None}
        infant_arv_proph = InfantArvProphModForm(data=inline_data)
        self.assertIn(u'You entered an ARV Code, please give the modification reason.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_not_needed(self):
        proph = InfantArvProphFactory(infant_visit=self.infant_visit, arv_status=NO_MODIFICATIONS)
        inline_data = {'infant_arv_proph': proph.id,
                       'arv_code': 'Nevirapine',
                       'dose_status': 'New',
                       'modification_date': date.today(),
                       'modification_code': 'Initial dose'}
        infant_arv_proph = InfantArvProphModForm(data=inline_data)
        self.assertIn(u'You did NOT indicate that medication was modified, so do not ENTER arv inline.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_azt_initiated(self):
        """Check that the azt dose is not initiated more than once"""
        self.infant_birth_arv.azt_discharge_supply = YES
        proph = InfantArvProphFactory(infant_visit=self.infant_visit, arv_status=MODIFIED)
        inline_data = {'infant_arv_proph': proph.id,
                       'arv_code': 'Zidovudine',
                       'dose_status': 'New',
                       'modification_date': date.today(),
                       'modification_code': 'Initial dose'}
        infant_arv_proph = InfantArvProphModForm(data=inline_data)
        self.assertIn(
            u'Infant birth ARV shows that infant was discharged with an additional dose of AZT, '
            'AZT cannot be initiated again.',
            infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_azt_different(self):
        """Check that the dose being modified is the same one infant was discharged with."""
        proph = InfantArvProphFactory(infant_visit=self.infant_visit, arv_status=MODIFIED)
        inline_data = {'infant_arv_proph': proph.id,
                       'arv_code': 'Nevarapine',
                       'dose_status': 'New',
                       'modification_date': date.today(),
                       'modification_code': 'Initial dose'}
        infant_arv_proph = InfantArvProphModForm(data=inline_data)
        self.assertIn(
            u'Infant birth ARV shows that infant was discharged with an additional dose of AZT, '
            'Arv Code should be AZT',
            infant_arv_proph.errors.get('__all__'))
