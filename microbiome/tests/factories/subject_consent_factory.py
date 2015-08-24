import factory
from django.utils import timezone
from edc_registration.tests.factories import RegisteredSubjectFactory

from ...models import SubjectConsent
from .maternal_eligibility_pre_factory import MaternalEligibilityPreFactory

class SubjectConsentFactory(factory.DjangoModelFactory):

    class Meta:
        model = SubjectConsent

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    maternal_eligibility_pre = factory.SubFactory(MaternalEligibilityPreFactory)
    gender = 'M'
    dob = dob = timezone.datetime(1980, 1, 10).date()
    initials = 'XX'
    subject_identifier = None
    consent_datetime = timezone.now()
    may_store_samples = 'Yes'
    is_literate = 'Yes'
    is_incarcerated = 'No'
    consent_version_on_entry = 1
    consent_version_recent = 1
    language = 'en'
    citizen = 'Yes'
    is_verified = False
    identity = factory.Sequence(lambda n: 'identity{0}'.format(n))
    identity_type = (('OMANG', 'Omang'), ('DRIVERS', "Driver's License"), ('PASSPORT', 'Passport'), ('OMANG_RCPT', 'Omang Receipt'), ('OTHER', 'Other'))[0][0]
    is_signed = True
