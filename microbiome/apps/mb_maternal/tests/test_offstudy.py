from dateutil.relativedelta import relativedelta
from datetime import date

from django.utils import timezone

from edc_meta_data.models import CrfMetaData
from edc_appointment.models import Appointment
from edc_constants.constants import YES, NO, POS, NEG, UNKEYED, NOT_APPLICABLE, SCHEDULED,\
    COMPLETED_PROTOCOL_VISIT

from microbiome.apps.mb.constants import MIN_AGE_OF_CONSENT
from microbiome.apps.mb_maternal.forms import MaternalOffStudyForm
from microbiome.apps.mb_maternal.models.maternal_visit import MaternalVisit
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory, MaternalOffStudyFactory
from microbiome.apps.mb_maternal.tests.factories.antenatal_enrollment_factory import AntenatalEnrollmentFactory
from microbiome.apps.mb_maternal.tests.factories.maternal_visit_factory import MaternalVisitFactory

from .base_maternal_test_case import BaseMaternalTestCase


class TestOffStudy(BaseMaternalTestCase):

    def setUp(self):
        super(TestOffStudy, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

        self.data = {
            'registered_subject': self.registered_subject.id,
            'reason': 'not_{}'.format(MIN_AGE_OF_CONSENT),
            'has_scheduled_data': YES,
            'maternal_visit': None,
            'offstudy_date': timezone.now().date()}

    def test_1000M_metadata_set_to_offstudy_if_not_ante(self):
        """Asserts ineligible at postnatal creates 1000M off study visit and makes off study form required."""
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=NO)
        self.assertFalse(postnatal_enrollment.is_eligible)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        MaternalVisit.objects.get(appointment=appointment, reason=COMPLETED_PROTOCOL_VISIT)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=UNKEYED,
            crf_entry__app_label='mb_maternal',
            crf_entry__model_name='maternaloffstudy',
            appointment=appointment).count(), 1)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='2000M')
        self.assertRaises(MaternalVisit.DoesNotExist, MaternalVisit.objects.get, appointment=appointment)

    def test_2000M_metadata_set_to_offstudy(self):
        """Asserts eligible at antenatal but ineligible at postnatal creates 2000M
        off study visit and makes off study form required."""
        antenatal_enrollment = AntenatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_date=date.today(),
            rapid_test_result=NEG)
        self.assertTrue(antenatal_enrollment.is_eligible)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        MaternalVisitFactory(
            appointment=appointment, reason=SCHEDULED)
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=NO)
        self.assertFalse(postnatal_enrollment.is_eligible)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='2000M')
        with self.assertRaises(MaternalVisit.DoesNotExist):
            try:
                MaternalVisit.objects.get(appointment=appointment, reason=COMPLETED_PROTOCOL_VISIT)
            except:
                pass
            else:
                raise MaternalVisit.DoesNotExist
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=UNKEYED,
            entry__app_label='mb_maternal',
            entry__model_name='maternaloffstudy',
            appointment=appointment).count(), 1)

    def test_offstudy2(self):
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(
            appointment=appointment,
            reason=COMPLETED_PROTOCOL_VISIT)
        MaternalOffStudyFactory(
            registered_subject=appointment.registered_subject,
            report_datetime=timezone.now(),
            offstudy_date=date.today(),
            maternal_visit=maternal_visit)
        self.assertEqual(
            Appointment.objects.filter(
                registered_subject=self.registered_subject).count(), 1)

    def test_offstudy3(self):
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(
            appointment=appointment,
            report_datetime=timezone.now(),
            reason=COMPLETED_PROTOCOL_VISIT)
        MaternalOffStudyFactory(
            registered_subject=appointment.registered_subject,
            maternal_visit=maternal_visit,
            report_datetime=timezone.now(),
            offstudy_date=date.today())
        self.assertEqual(Appointment.objects.filter(
            registered_subject=self.registered_subject).count(), 1)

    def test_validate_offstudy_date(self):
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(
            appointment=appointment,
            reason=COMPLETED_PROTOCOL_VISIT)
        self.data['maternal_visit'] = maternal_visit.id
        self.data['offstudy_date'] = date(2015, 10, 6)
        offstudy_form = MaternalOffStudyForm(data=self.data)
        self.assertIn(
            "Off study date cannot be before consent date",
            offstudy_form.errors.get("__all__"))

    def test_validate_offstudy_date_consent_datetime(self):
        self.maternal_consent.consent_datetime = timezone.now() - relativedelta(weeks=1)
        self.maternal_consent.save()
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(
            appointment=appointment, reason=COMPLETED_PROTOCOL_VISIT)
        self.data['maternal_visit'] = maternal_visit.id
        self.data['offstudy_date'] = timezone.now() - relativedelta(weeks=2)
        offstudy_form = MaternalOffStudyForm(data=self.data)
        self.assertIn(
            "Off study date cannot be before consent date",
            offstudy_form.errors.get("__all__"))
