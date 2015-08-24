import factory
from datetime import datetime, date
from edc.testing.tests.factories.test_consent_factory import BaseConsentFactory
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from ...models import SubjectConsent
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory


class SubjectConsentFactory(BaseConsentFactory):

    class Meta:
        model = SubjectConsent

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    gender = 'M'
    dob = date(1980, 01, 01)
    initials = 'XX'
    subject_identifier = None
    consent_datetime = datetime.today()
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
