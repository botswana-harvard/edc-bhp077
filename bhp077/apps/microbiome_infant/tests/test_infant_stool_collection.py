from django.test import TestCase
from django.utils import timezone

from edc.subject.registration.models import RegisteredSubject
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc_constants.constants import YES, NO, NEG, NOT_APPLICABLE

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_infant.forms import InfantStoolCollectionForm
from bhp077.apps.microbiome_infant.tests.factories import InfantBirthFactory, InfantVisitFactory
from bhp077.apps.microbiome_lab.tests.factories import InfantRequistionFactory
from bhp077.apps.microbiome_infant.visit_schedule import InfantBirthVisitSchedule
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile, InfantProfile
from bhp077.apps.microbiome_maternal.tests.factories import (
    MaternalConsentFactory, MaternalLabourDelFactory, MaternalEligibilityFactory,
    MaternalVisitFactory, PostnatalEnrollmentFactory)
from bhp077.apps.microbiome_maternal.visit_schedule import PostnatalEnrollmentVisitSchedule
from bhp077.apps.microbiome_infant.constants import REALTIME


class TestInfantStoolCollection(TestCase):

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

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            verbal_hiv_status=NEG,
            evidence_hiv_status=YES)
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
            visit_definition__code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.infant_requisition = InfantRequistionFactory(
            infant_visit=self.infant_visit,
            panel='')
        self.data = {
            'report_datetime': timezone.now(),
            'infant_visit': self.infant_visit.id,
            'sample_obtained': NO,
            'nappy_type': NOT_APPLICABLE,
            'other_nappy': '',
            'stool_colection': NOT_APPLICABLE,
            'stool_colection_time': '',
            'stool_stored': NOT_APPLICABLE,
            'past_diarrhea': NO,
            'diarrhea_past_24hrs': NOT_APPLICABLE,
            'antibiotics_7days': NO,
            'antibiotic_dose_24hrs': NOT_APPLICABLE
        }

    def test_sample_obtained_1(self):
        """If sample was obtained then nappy type cannot be N/A"""
        self.data['sample_obtained'] = YES
        form = InfantStoolCollectionForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Sample is indicated to have been obtained today, Nappy type CANNOT be Not Applicable.', errors)

    def test_sample_obtained_2(self):
        """If sample was stored, then should indicate when the sample was obtained"""
        self.data['sample_obtained'] = YES
        self.data['nappy_type'] = 'cloth nappy'
        form = InfantStoolCollectionForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Sample is indicated to have been obtained today, collection time CANNOT be not Applicable.',
                      errors)

    def test_sample_obtained_3(self):
        """If sample was obtained, have to indicate if sample was stored"""
        self.data['sample_obtained'] = YES
        self.data['nappy_type'] = 'cloth nappy'
        self.data['stool_colection'] = 'brought'
        form = InfantStoolCollectionForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Sample is stated to have been obtained today, please indicate if the sample was stored.', errors)

    def test_sample_obtained_4(self):
        self.data['nappy_type'] = 'cloth nappy'
        form = InfantStoolCollectionForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Sample is indicated to have NOT been collected, you CANNOT '
                      'specify the nappy type. Please correct.', errors)

    def test_sample_obtained_5(self):
        self.data['stool_colection'] = 'brought'
        form = InfantStoolCollectionForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Sample is indicated to have NOT been obtained today, you cannot specify the '
                      'collection time.', errors)

    def test_sample_obtained_6(self):
        self.data['stool_stored'] = YES
        form = InfantStoolCollectionForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Sample is stated to have been NOT obtained today, you cannot specify if the '
                      'sample was stored.', errors)

    def test_collection_time_1(self):
        self.data['sample_obtained'] = YES
        self.data['nappy_type'] = 'cloth nappy'
        self.data['stool_colection'] = 'brought'
        self.data['stool_stored'] = YES
        form = InfantStoolCollectionForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Please specify the number of hours that stool was collected.', errors)

    def test_collection_time_2(self):
        self.data['sample_obtained'] = YES
        self.data['nappy_type'] = 'cloth nappy'
        self.data['stool_colection'] = REALTIME
        self.data['stool_colection_time'] = 5
        self.data['stool_stored'] = YES
        form = InfantStoolCollectionForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You have stated that stool was collected real-time. You cannot indicate the number of hour ago '
                      'the stool was collected.', errors)

    def test_diarrhea_1(self):
        self.data['past_diarrhea'] = YES
        form = InfantStoolCollectionForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You have indicated the infant had diarrhea in the past 7 days, please '
                      'indicate if occurred in the past 24 hours.', errors)

    def test_diarrhea_2(self):
        self.data['diarrhea_past_24hrs'] = YES
        form = InfantStoolCollectionForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You have stated the infant did NOT have diarrhea in the past 7 days, '
                      'you cannot indicate if it occurred in the past 24 hours.', errors)

    def test_antibiotics_1(self):
        self.data['antibiotics_7days'] = YES
        form = InfantStoolCollectionForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You have indicated the infant took antibiotics in the past 7 days, please '
                      'indicate if taken in the past 24 hours.', errors)

    def test_antibiotics_2(self):
        self.data['antibiotic_dose_24hrs'] = YES
        form = InfantStoolCollectionForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You have stated the infant did NOT take antibiotics in the past 7 days, '
                      'you cannot indicate antibiotics were taken in the past 24 hours.', errors)

    def test_stool_requisition_and_no_stool_obtained(self):
        self.infant_requisition = InfantRequistionFactory(
            requisition_datetime=timezone.now(), infant_visit=self.infant_visit,
            panel__name='Stool storage', is_drawn=YES, drawn_datetime=timezone.now())
        self.data['sample_obtained'] = NO
        form = InfantStoolCollectionForm(data=self.data)
        self.assertIn('Stool requisition is drawn with id {}. Sample obtained cannot be {}'.format(self.infant_requisition.requisition_identifier,
                                                                                                   self.data['sample_obtained']), form.errors.get('__all__'))
