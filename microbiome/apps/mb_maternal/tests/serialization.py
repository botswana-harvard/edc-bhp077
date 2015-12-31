from django.core import serializers
from django.utils import timezone

from edc_appointment.models import Appointment
from edc_base.encrypted_fields import FieldCryptor
from edc_constants.choices import POS, YES, NO

from microbiome.apps.mb_maternal.models import MaternalDemographics
from microbiome.apps.mb_maternal.tests.factories import (
    MaternalEligibilityFactory, MaternalConsentFactory,
    SpecimenConsentFactory, AntenatalEnrollmentFactory,
    MaternalVisitFactory, MaternalLocatorFactory)

from .base_maternal_test_case import BaseMaternalTestCase


# TODO: need to rewrite these tests
class SerializeToTransaction(object):
    pass


class TestSerialization(BaseMaternalTestCase):

    def test_serialize_deserialize(self):
        """Confirms all models have a get_by_natural_key manager method."""
        maternal_eligibility = MaternalEligibilityFactory()
        maternal_consent = MaternalConsentFactory(registered_subject=maternal_eligibility.registered_subject)
        specimen_consent = SpecimenConsentFactory(registered_subject=maternal_consent.registered_subject)
        antenatal_enrollment = AntenatalEnrollmentFactory(
            registered_subject=specimen_consent.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NO)
        appointment = Appointment.objects.get(
            registered_subject=antenatal_enrollment.registered_subject,
            visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment)
        maternal_locator = MaternalLocatorFactory(
            maternal_visit=maternal_visit,
            registered_subject=antenatal_enrollment.registered_subject,)
        maternal_demographics = MaternalDemographics.objects.create(
            maternal_visit=maternal_visit,
            report_datetime=timezone.now(),
            marital_status='Single',
            ethnicity='Black African',
            highest_education='Tertiary',
            current_occupation='Student',
            provides_money='Mother',
            money_earned='P1001-5000 per month / P212 - 1157 per week',
            own_phone=YES,
            house_electrified=YES,
            house_fridge=YES,
            cooking_method='Gas or electric stove',
            toilet_facility='Indoor toilet',
            house_people_number=1,
            house_type='Formal: Tin-roofed, concrete walls')
        instances = []
        instances.append(maternal_eligibility)
        instances.append(maternal_consent)
        instances.append(specimen_consent)
        instances.append(antenatal_enrollment)
        instances.append(maternal_visit)
        instances.append(maternal_locator)
        instances.append(maternal_demographics)
        for obj in instances:
            natural_key = obj.natural_key()
            get_obj = obj.__class__.objects.get_by_natural_key(*natural_key)
            self.assertEqual(obj.pk, get_obj.pk)

        for obj in instances:
            outgoing_transaction = SerializeToTransaction().serialize(obj.__class__, obj, False, True, 'default')
            for transaction in serializers.deserialize(
                    "json", FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx)):
                self.assertEqual(transaction.object.pk, obj.pk)
