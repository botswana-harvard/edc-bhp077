from django.utils import timezone
from datetime import date

from edc_registration.models import RegisteredSubject
from edc_appointment.models import Appointment
from edc_constants.constants import YES, POS, NO, UNKNOWN, NOT_APPLICABLE

from microbiome.apps.mb.constants import INFANT
from microbiome.apps.mb_infant.forms import (InfantArvProphForm, InfantArvProphModForm)
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory, MaternalVisitFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory

from microbiome.apps.mb_infant.tests.factories import (InfantBirthFactory, InfantVisitFactory)

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
        self.data['arv_status'] = 'modified'
        infant_arv_proph = InfantArvProphForm(data=self.data)
        self.assertIn(u'Infant was not taking prophylactic arv, prophylaxis should be Not Applicable.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod(self):
        """Test if the infant arv status was modified but no Arv Code given on inline."""
        self.data['prophylatic_nvp'] = YES
        self.data['arv_status'] = 'modified'
        infant_arv_proph = InfantArvProphForm(data=self.data)
        self.assertIn(u'You indicated that the infant arv was modified, please give a valid Arv Code',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_dose_status(self):
        self.data['arv_code'] = 'Nevirapine'
        self.data['dose_status'] = None
        infant_arv_proph = InfantArvProphModForm(data=self.data)
        self.assertIn(u'You entered an ARV Code, please give the dose status.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_date(self):
        self.data['arv_code'] = 'Nevirapine'
        self.data['dose_status'] = 'New'
        self.data['modification_date'] = None
        infant_arv_proph = InfantArvProphModForm(data=self.data)
        self.assertIn(u'You entered an ARV Code, please give the modification date.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_infant_arv_proph_mod_code(self):
        self.data['arv_code'] = 'Nevirapine'
        self.data['dose_status'] = 'New'
        self.data['modification_date'] = date.today()
        self.data['modification_code'] = None
        infant_arv_proph = InfantArvProphModForm(data=self.data)
        self.assertIn(u'You entered an ARV Code, please give the modification reason.',
                      infant_arv_proph.errors.get('__all__'))
