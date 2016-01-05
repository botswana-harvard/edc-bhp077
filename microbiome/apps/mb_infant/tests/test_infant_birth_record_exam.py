from django.test import TestCase
from django.utils import timezone
from datetime import datetime

from microbiome.apps.mb_infant.forms import InfantBirthExamForm

from edc_registration.models import RegisteredSubject
from edc_lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc_rule_groups.classes import site_rule_groups
from edc_lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc_appointment.models import Appointment
from edc_constants.constants import YES, NO, POS

from microbiome.apps.mb import MicrobiomeConfiguration
from microbiome.apps.mb.constants import INFANT
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory, MaternalVisitFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory
from microbiome.apps.mb_lab.lab_profiles import MaternalProfile, InfantProfile

from microbiome.apps.mb_maternal.visit_schedule import (
    AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule)
from microbiome.apps.mb_infant.visit_schedule import InfantBirthVisitSchedule
from microbiome.apps.mb_infant.tests.factories import (InfantBirthFactory, InfantVisitFactory)


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
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
        )
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M'
        )
        maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)

        self.registered_subject_infant = RegisteredSubject.objects.get(
            subject_type=INFANT, relative_identifier=self.registered_subject.subject_identifier
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
            'general_activity': 'NORMAL',
            'abnormal_activity': '',
            'physical_exam_result': 'NORMAL',
            'heent_exam': YES,
            'heent_no_other': '',
            'resp_exam': YES,
            'resp_exam_other': '',
            'cardiac_exam': YES,
            'cardiac_exam_other': '',
            'abdominal_exam': YES,
            'abdominal_exam_other': '',
            'skin_exam': YES,
            'skin_exam_other': '',
            'macular_papular_rash': YES,
            'macular_papular_rash_other': '',
            'neurologic_exam': YES,
            'neuro_exam_other': '',
            'other_exam_info': 'NA',
        }

    def test_validate_general_activity1(self):
        self.data['general_activity'] = 'ABNORMAL'
        self.data['abnormal_activity'] = ''
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        errors = ''.join(self.infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'If abnormal, please specify.', errors)

    def test_validate_general_activity2(self):
        self.data['general_activity'] = 'NORMAL'
        self.data['abnormal_activity'] = 'looks sideways'
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        errors = ''.join(self.infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'You indicated that there was NO abnormality in general activity', errors)

    def test_validate_heent_exam1(self):
        self.data['heent_exam'] = YES
        self.data['heent_no_other'] = 'HEENT problems'
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        errors = ''.join(self.infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'If HEENT Exam is normal, Do not answer the following Question (Q7).', errors)

    def test_validate_heent_exam2(self):
        self.data['heent_exam'] = NO
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        errors = ''.join(self.infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q7.', errors)

    def test_validate_resp_exam1(self):
        self.data['resp_exam'] = YES
        self.data['resp_exam_other'] = 'Asthma'
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        errors = ''.join(self.infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'If Respiratory Exam is normal, Do not answer the following Question (Q9).', errors)

    def test_validate_resp_exam2(self):
        self.data['resp_exam'] = NO
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        errors = ''.join(self.infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q9.', errors)

    def test_validate_cardiac_exam1(self):
        self.data['cardiac_exam'] = YES
        self.data['cardiac_exam_other'] = 'Palpitations'
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        errors = ''.join(self.infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'If Cardiac Exam is normal, Do not answer the following Question (Q11).', errors)

    def test_validate_cardiac_exam2(self):
        self.data['cardiac_exam'] = NO
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        errors = ''.join(self.infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q11.', errors)

    def test_validate_report_datetime_invalid(self):
        self.data['cardiac_exam'] = NO
        self.data['report_datetime'] = datetime(2015, 11, 18, 8, 29, 44)
        self.infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        errors = ''.join(self.infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'Report_Datetime CANNOT be before consent datetime', errors)

    def test_abdominal_exam_1(self):
        self.data['abdominal_exam'] = NO
        infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        errors = ''.join(infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q13.', errors)

    def test_abdominal_exam_2(self):
        self.data['abdominal_exam'] = YES
        self.data['abdominal_exam_other'] = 'TOO BIG'
        infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        errors = ''.join(infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'If Abdominal Exam is normal', errors)

    def test_skin_exam_1(self):
        self.data['skin_exam'] = NO
        infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        errors = ''.join(infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q15.', errors)

    def test_skin_exam_2(self):
        self.data['skin_exam'] = YES
        self.data['skin_exam_other'] = 'lesions'
        infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        errors = ''.join(infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'If Skin Exam is normal', errors)

    def test_rash_exam_1(self):
        self.data['macular_papular_rash'] = YES
        self.data['macular_papular_rash_other'] = 'ringworm'
        infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        errors = ''.join(infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'If macular / papular rash Exam is normal', errors)

    def test_rash_exam_2(self):
        self.data['macular_papular_rash'] = NO
        infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        errors = ''.join(infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q17.', errors)

    def test_neuro_exam_1(self):
        self.data['neurologic_exam'] = YES
        self.data['neuro_exam_other'] = 'bipolar'
        infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        errors = ''.join(infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'If Neurological Exam is normal', errors)

    def test_neuro_exam_2(self):
        self.data['neurologic_exam'] = NO
        infant_birth_record_arv_form = InfantBirthExamForm(data=self.data)
        errors = ''.join(infant_birth_record_arv_form.errors.get('__all__'))
        self.assertIn(u'Provide answer to Q19.', errors)
