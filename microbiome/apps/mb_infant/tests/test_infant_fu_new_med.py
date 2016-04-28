import datetime
from django.utils import timezone
from datetime import date

from edc_registration.models import RegisteredSubject
from edc_appointment.models import Appointment
from edc_constants.constants import YES, POS, NO, OTHER

from microbiome.apps.mb.constants import INFANT, NO_MODIFICATIONS
from microbiome.apps.mb_infant.forms import (InfantFuNewMedForm, InfantFuNewMedItemsForm)
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory, MaternalVisitFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory

from microbiome.apps.mb_infant.tests.factories import (InfantBirthFactory, InfantVisitFactory,
                                                       InfantFuNewMedFactory, InfantFuNewMedItemsFactory)

from .base_test_case import BaseTestCase


class TestInfantFuNewMed(BaseTestCase):

    def setUp(self):
        super(TestInfantFuNewMed, self).setUp()
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
            'new_medications': YES,
        }

    def test_validate_new_medications_yes(self):
        infant_fu_med = InfantFuNewMedFactory(infant_visit=self.infant_visit, new_medications=YES)
        inline_data = {'infant_fu_med': infant_fu_med.id,
                       'date_first_medication': timezone.now(),
                       'stop_date': timezone.now(),
                       'drug_route': '3', }
        infant_fu_items = InfantFuNewMedItemsForm(data=inline_data)
        self.assertIn(u'You have indicated that participant took medications. Please provide them.',
                      infant_fu_items.errors.get('__all__'))

    def test_validate_new_medications_no(self):
        infant_fu_med = InfantFuNewMedFactory(infant_visit=self.infant_visit, new_medications=NO)
        inline_data = {'infant_fu_med': infant_fu_med.id,
                       'medication': 'Acyclovir',
                       'date_first_medication': timezone.now(),
                       'stop_date': timezone.now(),
                       'drug_route': '3', }
        infant_fu_items = InfantFuNewMedItemsForm(data=inline_data)
        self.assertIn(
            u'You indicated that no medications were taken. You cannot provide the medication. Please correct',
            infant_fu_items.errors.get('__all__'))

    def test_validate_stop_date(self):
        infant_fu_med = InfantFuNewMedFactory(infant_visit=self.infant_visit, new_medications=YES)
        inline_data = {'infant_fu_med': infant_fu_med.id,
                       'medication': 'Acyclovir',
                       'date_first_medication': timezone.now() + datetime.timedelta(days=7),
                       'stop_date': timezone.now(),
                       'drug_route': '3', }
        infant_fu_items = InfantFuNewMedItemsForm(data=inline_data)
        self.assertIn(
            u'You have indicated that medication stop date is before its start date. Please correct.',
            infant_fu_items.errors.get('__all__'))

    def test_validate_other_yes(self):
        infant_fu_med = InfantFuNewMedFactory(infant_visit=self.infant_visit, new_medications=YES)
        inline_data = {'infant_fu_med': infant_fu_med.id,
                       'medication': OTHER,
                       'date_first_medication': timezone.now(),
                       'stop_date': timezone.now(),
                       'drug_route': '3', }
        infant_fu_items = InfantFuNewMedItemsForm(data=inline_data)
        self.assertIn(u'Please specify other medication.', infant_fu_items.errors.get('__all__'))

    def test_validate_other_no(self):
        infant_fu_med = InfantFuNewMedFactory(infant_visit=self.infant_visit, new_medications=YES)
        inline_data = {'infant_fu_med': infant_fu_med.id,
                       'medication': 'Acyclovir',
                       'other_medication': 'Vicks',
                       'date_first_medication': timezone.now(),
                       'stop_date': timezone.now(),
                       'drug_route': '3', }
        infant_fu_items = InfantFuNewMedItemsForm(data=inline_data)
        self.assertIn(u'Please select Other in Medication in when if Other medication is being record.',
                      infant_fu_items.errors.get('__all__'))
