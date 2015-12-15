from django.db.models import signals
from datetime import datetime, timedelta, date

from django.core import serializers
from django.db.models import get_app, get_models
from django.test import TestCase

from edc.subject.appointment.models import Appointment
from edc_constants.constants import YES, POS

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.rule_groups.classes import site_rule_groups
from edc.subject.lab_tracker.classes import site_lab_tracker

from edc.core.crypto_fields.classes import FieldCryptor
from edc.device.sync.classes import SerializeToTransaction
from edc.subject.registration.models import RegisteredSubject

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_infant.tests.factories import InfantBirthFactory
from bhp077.apps.microbiome_infant.visit_schedule import InfantBirthVisitSchedule
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile, InfantProfile
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from bhp077.apps.microbiome_maternal.tests.factories import MaternalEligibilityFactory
from bhp077.apps.microbiome_maternal.tests.factories import PostnatalEnrollmentFactory
from bhp077.apps.microbiome_maternal.tests.factories.maternal_visit_factory import MaternalVisitFactory
from bhp077.apps.microbiome_maternal.visit_schedule import (
    AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule)


class TestNaturalKey(TestCase):

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

        self.registered_subject_infant = RegisteredSubject.objects.get(
            subject_type='infant', relative_identifier=self.registered_subject.subject_identifier)
        self.infant_birth = InfantBirthFactory(
            registered_subject=self.registered_subject_infant, maternal_labour_del=maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject_infant,
            visit_definition__code='2000')

    def test_has_natural_key_method(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        app = get_app('microbiome_infant')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                self.assertTrue('natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))

    def test_has_get_by_natural_key(self):
        """Confirms all models have a get_by_natural_key manager method."""
        app = get_app('microbiome_infant')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                self.assertTrue('get_by_natural_key' in dir(model.objects), 'get_by_natural_key key not found in {0}'.format(model._meta.object_name))

    def test_serializing_deserialing_models(self):
        print 'test serializing/deserializing {0}'.format(self.infant_birth._meta.object_name)
        outgoing_transaction = SerializeToTransaction().serialize(self.infant_birth.__class__, self.infant_birth, False, True, 'default')
        print outgoing_transaction
        # pp.pprint(FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx))
        for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx)):
            self.assertEqual(transaction.object.pk, self.infant_birth.pk)
