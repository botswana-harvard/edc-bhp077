from django.test import TestCase
from django.db.models import get_app, get_models

from edc.subject.lab_tracker.classes import site_lab_tracker
from edc_lab.lab_profile.classes import site_lab_profiles
from edc_lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile

from edc_rule_groups.classes import site_rule_groups

from microbiome.apps.mb import AppConfiguration
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory
from microbiome.apps.mb_lab.lab_profiles import MaternalProfile
from microbiome.apps.mb_maternal.visit_schedule import AntenatalEnrollmentVisitSchedule


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
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject
        self.data = {
            'registered_subject': self.registered_subject}

    def test_p1(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        app = get_app('mb_lab')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                self.assertTrue(
                    'natural_key' in dir(model),
                    'natural key not found in {0}'.format(model._meta.object_name))

    def test_p2(self):
        """Confirms all models have a get_by_natural_key manager method."""
        app = get_app('mb_lab')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                self.assertTrue(
                    'get_by_natural_key' in dir(model.objects),
                    'get_by_natural_key key not found in {0}'.format(model._meta.object_name))
