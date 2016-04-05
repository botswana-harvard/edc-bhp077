from datetime import timedelta
from django.utils import timezone

from edc_registration.models import RegisteredSubject
from edc_consent.models import ConsentType

from microbiome.apps.mb_maternal.forms import MaternalConsentForm

from .base_test_case import BaseTestCase
from .factories import MaternalEligibilityFactory, MaternalConsentFactory


class TestMaternalConsent(BaseTestCase):

    def setUp(self):
        super(TestMaternalConsent, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.registered_subject = RegisteredSubject.objects.get(
            pk=self.maternal_eligibility.registered_subject.pk)

    def test_identity_wrong_gender(self):
        """Test that Omang number reflects the correct gender digit."""
        consent = MaternalConsentFactory(
            identity='123411234', confirm_identity='123411234',
            registered_subject=self.maternal_eligibility.registered_subject)
        consent_form = MaternalConsentForm(data=consent.__dict__)
        errors = ''.join(consent_form.errors.get('__all__'))
        self.assertIn('Identity provided indicates participant is Male.', errors)

    def test_registered_subject_registration_datetime_on_post_save(self):
        self.assertIsNone(self.registered_subject.registration_datetime)
        MaternalConsentFactory(
            consent_datetime=timezone.now(),
            identity='123411234',
            confirm_identity='123411234',
            registered_subject=self.registered_subject)
        registered_subject = RegisteredSubject.objects.get(pk=self.registered_subject.pk)
        self.assertIsNotNone(registered_subject.registration_datetime)

    def test_save_next_consent_version(self):
        consent_current_version = MaternalConsentFactory(
            identity='123411234', confirm_identity='123411234',
            registered_subject=self.maternal_eligibility.registered_subject,
            report_datetime=timezone.now())
        consent_type_latest = ConsentType.objects.all().order_by('-version').first()
        ConsentType.objects.create(
            app_label='mb_maternal',
            model_name='maternalconsent',
            start_datetime=consent_type_latest.end_datetime + timedelta(days=1),
            end_datetime=consent_type_latest.end_datetime + timedelta(days=3),
            version=int(consent_current_version.version) + 1)
        consent_next_version = MaternalConsentFactory(
            identity='123411234', confirm_identity='123411234',
            registered_subject=self.maternal_eligibility.registered_subject,
            consent_datetime=consent_type_latest.end_datetime + timedelta(days=2))
        self.assertEqual(int(consent_current_version.version) + 1, int(consent_next_version.version))
        self.assertEqual(consent_current_version.subject_identifier, consent_next_version.subject_identifier)

    def test_have_latest_consent(self):
        consent_type_latest = ConsentType.objects.all().order_by('-version').first()
        consent_type_latest.start_datetime = timezone.now() - timedelta(days=6)
        consent_type_latest.end_datetime = timezone.now() - timedelta(days=3)
        consent_type_latest.save()
        consent_current_version = MaternalConsentFactory(
            identity='123411234', confirm_identity='123411234',
            registered_subject=self.maternal_eligibility.registered_subject,
            consent_datetime=timezone.now() - timedelta(days=4))
        ConsentType.objects.create(
            app_label='mb_maternal',
            model_name='maternalconsent',
            start_datetime=timezone.now() - timedelta(days=2),
            end_datetime=timezone.now() + timedelta(days=2),
            version=int(consent_current_version.version) + 1)
        self.assertFalse(self.maternal_eligibility.have_latest_consent)
        consent_current_version = MaternalConsentFactory(
            identity='123411234', confirm_identity='123411234',
            registered_subject=self.maternal_eligibility.registered_subject,
            consent_datetime=timezone.now())
        self.assertTrue(self.maternal_eligibility.have_latest_consent)

    def test_previous_consents(self):
        consent_current_version = MaternalConsentFactory(
            identity='123411234', confirm_identity='123411234',
            registered_subject=self.maternal_eligibility.registered_subject,
            report_datetime=timezone.now())
        ConsentType.objects.create(
            app_label='mb_maternal',
            model_name='maternalconsent',
            start_datetime=timezone.now() + timedelta(days=1),
            end_datetime=timezone.now() + timedelta(days=3),
            version=int(consent_current_version.version) + 1)
        self.assertEqual(self.maternal_eligibility.previous_consents.count(), 1)
