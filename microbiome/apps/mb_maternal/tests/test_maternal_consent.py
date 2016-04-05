from django.utils import timezone

from edc_registration.models import RegisteredSubject

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
