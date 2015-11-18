from django.test import TestCase
from django.utils import timezone
from datetime import datetime

from bhp077.apps.microbiome_infant.models import InfantVisit
from bhp077.apps.microbiome_infant.forms import InfantBirthExamForm

from edc.subject.registration.models import RegisteredSubject
from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc_constants.constants import NEW, YES, NO, POS, NEG, NOT_REQUIRED

from bhp077.apps.microbiome.constants import LIVE
from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_maternal.tests.factories import (MaternalEligibilityFactory, AntenatalEnrollmentFactory,
    MaternalVisitFactory)
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from bhp077.apps.microbiome_maternal.tests.factories import PostnatalEnrollmentFactory, SexualReproductiveHealthFactory
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile, InfantProfile
from bhp077.apps.microbiome_maternal.models import PostnatalEnrollment

from bhp077.apps.microbiome_maternal.visit_schedule import AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule
from bhp077.apps.microbiome_infant.visit_schedule import InfantBirthVisitSchedule
from bhp077.apps.microbiome_infant.tests.factories import \
    (InfantBirthFactory, InfantBirthDataFactory, InfantVisitFactory, InfantBirthFeedVaccineFactory)
from bhp077.apps.microbiome_infant.models import InfantBirth


class TestInfantBirthRecordExam(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
            site_lab_profiles.register(InfantProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        AntenatalEnrollmentVisitSchedule().build()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()
        InfantBirthVisitSchedule().build()

        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

        post = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            verbal_hiv_status=POS,
            evidence_hiv_status=YES,
        )
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M'
        )
        maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)

        self.registered_subject_infant = RegisteredSubject.objects.get(
            subject_type='infant', relative_identifier=self.registered_subject.subject_identifier
        )
        self.infant_birth = InfantBirthFactory(
            registered_subject=self.registered_subject_infant,
            maternal_labour_del=maternal_labour_del,
            gender='F',
        )
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject_infant,
            visit_definition__code='2000'
        )
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.data = {
            'report_datetime': timezone.now(),
            'infant_birth': self.infant_birth.id,
            'infant_visit': self.infant_visit.id,
            'infant_exam_date': timezone.now().date(),
            'gender': 'M',
            'general_activity': 'NORMAL',
            'abnormal_activity': 'SETSENO',
            'physical_exam_result': 'NORMAL',
            'heent_exam': YES,
            'heent_no_other': 'NA',
            'resp_exam': YES,
            'resp_exam_other': 'NA',
            'cardiac_exam': YES,
            'cardiac_exam_other': 'NA',
            'abdominal_exam': YES,
            'abdominal_exam_other': 'NA',
            'skin_exam': YES,
            'skin_exam_other': 'NA',
            'macular_papular_rash': YES,
            'macular_papular_rash_other': 'NA',
            'neurologic_exam': YES,
            'neuro_exam_other': 'NA',
            'other_exam_info': 'NA',
        }
    def test_clean_gender(self):
        #infant_birth = InfantBirth.objects.get(registered_subject=self.registered_subject_infant)
        print timezone.now().date()
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        self.assertIn(u'Gender mismatch you specified F for infant birth and infant birth exam M', self.infant_birth_record_arv_form.errors.get('__all__'))

    def test_validate_general_activity1(self):
        del self.data['abnormal_activity']
        self.data['general_activity'] = 'ABNORMAL'
        self.data['gender'] = 'F'
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        self.assertIn(u'If abnormal, please specify.', self.infant_birth_record_arv_form.errors.get('__all__'))

    def test_validate_general_activity2(self):
        #infant_birth = InfantBirth.objects.get(infant_visit=cleaned_data.get('infant_visit'))
        del self.data['abnormal_activity']
        self.data['general_activity'] = 'ABNORMAL'
        self.data['gender'] = 'F'
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        self.assertIn(u'If abnormal, please specify.', self.infant_birth_record_arv_form.errors.get('__all__'))

    def test_validate_heent_exam1(self):
        self.data['heent_exam'] = YES
        self.data['gender'] = 'F'
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        self.assertIn(u'If HEENT Exam is normal or not evaluated, Do not answer the following Question (Q10).',
                      self.infant_birth_record_arv_form.errors.get('__all__'))

    def test_validate_heent_exam2(self):
        self.data['heent_exam'] = NO
        self.data['gender'] = 'F'
        del self.data['heent_no_other']
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        self.assertIn(u'Provide answer to Q10.', self.infant_birth_record_arv_form.errors.get('__all__'))


    def test_validate_resp_exam1(self):
        self.data['resp_exam'] = YES
        self.data['resp_exam_other'] = 'NA'
        self.data['gender'] = 'F'
        del self.data['heent_no_other']
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        self.assertIn(u'If Respiratory Exam is normal, Do not answer the following Question (Q12).',
                      self.infant_birth_record_arv_form.errors.get('__all__'))

    def test_validate_resp_exam2(self):
        self.data['resp_exam'] = NO
        self.data['gender'] = 'F'
        del self.data['resp_exam_other']
        del self.data['heent_no_other']
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        self.assertIn(u'Provide answer to Q12.', self.infant_birth_record_arv_form.errors.get('__all__'))

    def test_validate_cardiac_exam1(self):
        self.data['cardiac_exam'] = YES
        self.data['gender'] = 'F'
        del self.data['resp_exam_other']
        del self.data['heent_no_other']
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        self.assertIn(u'If Cardiac Exam is normal, Do not answer the following Question (Q14).',
                      self.infant_birth_record_arv_form.errors.get('__all__'))

    def test_validate_cardiac_exam2(self):
        self.data['cardiac_exam'] = NO
        self.data['gender'] = 'F'
        del self.data['resp_exam_other']
        del self.data['heent_no_other']
        del self.data['cardiac_exam_other']
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        self.assertIn(u'Provide answer to Q14.',
                      self.infant_birth_record_arv_form.errors.get('__all__'))

    def test_validate_report_datetime_invalid(self):
        self.data['cardiac_exam'] = NO
        self.data['gender'] = 'F'
        self.data['report_datetime'] = datetime(2015, 11, 18, 8, 29, 44)
        del self.data['resp_exam_other']
        del self.data['heent_no_other']
        del self.data['cardiac_exam_other']
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        self.assertIn(u'Report_Datetime CANNOT be before consent datetime',
                      self.infant_birth_record_arv_form.errors.get('__all__'))

    def test_validate_report_datetime_valid(self):
        self.data['cardiac_exam'] = NO
        self.data['gender'] = 'F'
        self.data['report_datetime'] = timezone.now()
        del self.data['resp_exam_other']
        del self.data['heent_no_other']
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        self.assertTrue(self.infant_birth_record_arv_form.is_valid())

