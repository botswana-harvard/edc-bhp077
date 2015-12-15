from django.test import TestCase
from django.core import serializers
from django.db.models import get_app, get_models

from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.device.sync.classes import SerializeToTransaction
from edc.subject.rule_groups.classes import site_rule_groups
from edc.subject.appointment.models import Appointment

from edc_base.encrypted_fields import FieldCryptor
from edc_constants.choices import POS, YES, NO

from microbiome.apps.mb.app_configuration.classes import MicrobiomeConfiguration
from microbiome.apps.mb_maternal.tests.factories import (MaternalEligibilityFactory, MaternalConsentFactory,
                                                         SpecimenConsentFactory, AntenatalEnrollmentFactory,
                                                         MaternalVisitFactory, MaternalLocatorFactory)
from microbiome.apps.mb_lab.lab_profiles import MaternalProfile
from ..visit_schedule import AntenatalEnrollmentVisitSchedule


class NaturalKeyTests(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        AntenatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()

    def test_p1(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        app = get_app('mb_maternal')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                self.assertTrue(
                    'natural_key' in dir(model),
                    'natural key not found in {0}'.format(model._meta.object_name))

    def test_p2(self):
        """Confirms all models have a get_by_natural_key manager method."""
        app = get_app('mb_maternal')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                self.assertTrue(
                    'get_by_natural_key' in dir(model.objects),
                    'get_by_natural_key key not found in {0}'.format(model._meta.object_name))

    def test_serialisation_deserialize(self):
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
        instances = []
        instances.append(maternal_eligibility)
        instances.append(maternal_consent)
        instances.append(specimen_consent)
        instances.append(antenatal_enrollment)
        instances.append(maternal_visit)
        instances.append(maternal_locator)
        for obj in instances:
            natural_key = obj.natural_key()
            get_obj = obj.__class__.objects.get_by_natural_key(*natural_key)
            self.assertEqual(obj.pk, get_obj.pk)

        for obj in instances:
            outgoing_transaction = SerializeToTransaction().serialize(obj.__class__, obj, False, True, 'default')
            for transaction in serializers.deserialize(
                    "json", FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx)):
                self.assertEqual(transaction.object.pk, obj.pk)
