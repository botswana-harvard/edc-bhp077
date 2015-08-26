import factory
from django.utils import timezone

from ...models import SubjectConsent
from .maternal_screening_factory import MaternalScreeningFactory


class SubjectConsentFactory(factory.DjangoModelFactory):

    class Meta:
        model = SubjectConsent

    maternal_eligibility_pre = factory.SubFactory(MaternalScreeningFactory)
    subject_identifier = '077-35170005-2'
    gender = 'F'
    dob = dob = timezone.datetime(1980, 1, 10).date()
    initials = 'XX'
    subject_identifier = None
    first_name = factory.Sequence(lambda n: 'first_name{0}'.format(n))
    last_name = factory.Sequence(lambda n: 'last_name{0}'.format(n))
    subject_type = 'subject'
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
