from django.utils import timezone
from datetime import date

from edc_appointment.models import Appointment
from edc_constants.constants import NEW, YES, NEG, COMPLETED_PROTOCOL_VISIT, OFF_STUDY
from edc_meta_data.models import CrfMetaData
from edc_registration.models import RegisteredSubject
from edc_visit_schedule.classes.controller import site_visit_schedules

from microbiome.apps.mb.constants import MIN_AGE_OF_CONSENT, INFANT
from microbiome.apps.mb_maternal.tests.factories import (
    MaternalEligibilityFactory, MaternalVisitFactory)
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory
from microbiome.apps.mb_infant.tests.factories import (
    InfantBirthFactory, InfantVisitFactory, InfantOffStudyFactory)

from ..forms import InfantOffStudyForm

from .base_test_case import BaseTestCase


class TestOffStudy(BaseTestCase):

    def setUp(self):
        super(TestOffStudy, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.registered_subject = self.maternal_eligibility.registered_subject
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.registered_subject)

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
            registered_subject=self.registered_subject,
            visit_definition__code='2000M')
        maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)
        self.infant_registered_subject = RegisteredSubject.objects.get(
            relative_identifier=self.registered_subject.subject_identifier,
            subject_type=INFANT)
        self.infant_birth = InfantBirthFactory(
            registered_subject=self.infant_registered_subject,
            maternal_labour_del=maternal_labour_del)
        self.infant_appointment = Appointment.objects.get(
            registered_subject=self.infant_registered_subject,
            visit_definition__code='2000')

        self.data = {
            'registered_subject': self.registered_subject.id,
            'reason': 'not_{}'.format(MIN_AGE_OF_CONSENT),
            'has_scheduled_data': YES,
            'infant_visit': None,
            'offstudy_date': timezone.now().date(),
        }

    def test_offstudy_meta_data_created_on_visit(self):
        self.infant_visit = InfantVisitFactory(
            appointment=self.infant_appointment,
            study_status=OFF_STUDY,
            reason=COMPLETED_PROTOCOL_VISIT)
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=NEW,
                crf_entry__app_label='mb_infant',
                crf_entry__model_name='infantoffstudy',
                appointment=self.infant_appointment).count(), 1)

    def test_offstudy2(self):
        self.infant_visit = InfantVisitFactory(
            appointment=self.infant_appointment,
            study_status=OFF_STUDY,
            reason=COMPLETED_PROTOCOL_VISIT)
        infant_birth_visit_schedule = site_visit_schedules.get_visit_schedule('birth visit schedule')
        self.assertEqual(
            Appointment.objects.filter(
                registered_subject=self.infant_registered_subject).count(),
            len(infant_birth_visit_schedule.visit_definitions))
        InfantOffStudyFactory(
            report_datetime=timezone.now(),
            registered_subject=self.infant_appointment.registered_subject,
            infant_visit=self.infant_visit,
            offstudy_date=date.today())
        self.assertEqual(
            Appointment.objects.filter(
                registered_subject=self.infant_registered_subject).count(), 1)

    def test_validate_offstudy_date(self):

        self.infant_visit = InfantVisitFactory(
            appointment=self.infant_appointment,
            reason=COMPLETED_PROTOCOL_VISIT)
        self.data['infant_visit'] = self.infant_visit.id
        self.data['offstudy_date'] = date(2015, 10, 6)
        offstudy_form = InfantOffStudyForm(data=self.data)
        offstudy_form.is_valid()
        self.assertIn("Off study date cannot be before consent date", offstudy_form.errors.get("__all__"))
