from django.utils import timezone

from edc_appointment.models import Appointment
from edc_sync.tests import TestSerializeDeserialize
from edc_constants.constants import YES, NO, POS

from microbiome.apps.mb_maternal.tests.factories import (
    MaternalEligibilityFactory, MaternalConsentFactory, PostnatalEnrollmentFactory,
    SpecimenConsentFactory, AntenatalEnrollmentFactory, ReproductiveHealthFactory,
    MaternalVisitFactory, MaternalLocatorFactory, MaternalDemographicsFactory)

from .base_test_case import BaseTestCase


class TestSerializationDeserialization(BaseTestCase, TestSerializeDeserialize):

    def setUp(self):
        super(TestSerializationDeserialization, self).setUp()

    def get_model_instances(self):
        instances = []
        maternal_eligibility = MaternalEligibilityFactory()
        instances.append(maternal_eligibility)
        maternal_consent = MaternalConsentFactory(registered_subject=maternal_eligibility.registered_subject)
        instances.append(maternal_consent)
        specimen_consent = SpecimenConsentFactory(registered_subject=maternal_consent.registered_subject)
        instances.append(specimen_consent)
        antenatal_enrollment = AntenatalEnrollmentFactory(
            registered_subject=specimen_consent.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NO)
        instances.append(antenatal_enrollment)
        post_natal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=specimen_consent.registered_subject,
        )
        instances.append(post_natal_enrollment)
        appointment_1000 = Appointment.objects.get(
            registered_subject=antenatal_enrollment.registered_subject,
            visit_definition__code='1000M')
        instances.append(appointment_1000)
        maternal_visit_1000 = MaternalVisitFactory(appointment=appointment_1000)
        instances.append(maternal_visit_1000)
        maternal_locator = MaternalLocatorFactory(
            maternal_visit=maternal_visit_1000,
            registered_subject=antenatal_enrollment.registered_subject,)
        instances.append(maternal_locator)
        maternal_demographics = MaternalDemographicsFactory(
            maternal_visit=maternal_visit_1000,
        )
        instances.append(maternal_demographics)
        appointment_2000 = Appointment.objects.get(
            registered_subject=antenatal_enrollment.registered_subject,
            visit_definition__code='2000M')
        appointment_2000 = MaternalVisitFactory(appointment=appointment_2000)
        instances.append(appointment_2000)
        appointment_2010 = Appointment.objects.get(
            registered_subject=antenatal_enrollment.registered_subject,
            visit_definition__code='2010M')
        maternal_visit_2010 = MaternalVisitFactory(appointment=appointment_2010)
        instances.append(maternal_visit_2010)
        reproductive_health = ReproductiveHealthFactory(
            maternal_visit=maternal_visit_2010
        )
        instances.append(reproductive_health)
        return instances