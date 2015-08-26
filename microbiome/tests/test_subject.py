from django.test import TransactionTestCase
from django.core.exceptions import ValidationError

from microbiome.models import SubjectConsent

from .factories import MaternalScreeningFactory, SubjectConsentFactory


class TestSubject(TransactionTestCase):

    def test_consent(self):
        subject_consent = SubjectConsentFactory()
