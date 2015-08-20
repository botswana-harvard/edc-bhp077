from django.test import TransactionTestCase

from microbiome.models import SubjectConsent


class TestSubject(TransactionTestCase):

    def test_consent(self):
        subject_consent = SubjectConsent()
        print([f.name for f in subject_consent._meta.fields])
