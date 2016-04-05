from edc_appointment.models import Appointment
from edc_constants.choices import YES
from edc_constants.constants import UNSCHEDULED, SCHEDULED, POS

from microbiome.apps.mb_lab.models import MaternalRequisition
from microbiome.apps.mb_lab.models.aliquot import AliquotType

from microbiome.apps.mb_maternal.tests.factories import (PostnatalEnrollmentFactory, MaternalVisitFactory)
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory

from .factories import MaternalRequistionFactory

from ..models import Panel

from .base_test_case import BaseTestCase


class TestMaternalRequisitionModel(BaseTestCase):
    """Test eligibility of a mother for postnatal followup."""

    def setUp(self):
        super(TestMaternalRequisitionModel, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject,
            study_site=self.study_site)
        self.registered_subject = self.maternal_consent.registered_subject
        self.postnatal_enrollment = PostnatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            will_breastfeed=YES)
        self.panel = Panel.objects.get(name='Breast Milk (Storage)')
        self.aliquot_type = AliquotType.objects.get(alpha_code='WB')
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')

    def test_visit_reason_scheduled(self):
        maternal_visit = MaternalVisitFactory(appointment=self.appointment, reason=SCHEDULED)
        MaternalRequistionFactory(
            maternal_visit=maternal_visit,
            panel=self.panel,
            aliquot_type=self.aliquot_type)

    def test_visit_reason_unscheduled(self):
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='2000M')
        MaternalVisitFactory(appointment=self.appointment, reason=SCHEDULED)
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason=UNSCHEDULED)
        MaternalRequistionFactory(panel=self.panel,
                                  aliquot_type=self.aliquot_type,
                                  maternal_visit=maternal_visit)
        self.assertEqual(MaternalRequisition.objects.all().count(), 1)
