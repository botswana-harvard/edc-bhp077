import factory

from django.conf import settings
from django.utils import timezone
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from edc.core.bhp_variables.tests.factories import StudySiteFactory
from edc_constants.constants import YES, NO

from bhp077.apps.microbiome_maternal.models import MaternalConsent


class MaternalConsentFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalConsent

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    report_datetime = timezone.now()
    study_site = factory.SubFactory(StudySiteFactory)
    consent_datetime = timezone.now()
    first_name = "DIMO"
    last_name = "DIMO"
    initials = "DD"
    dob = timezone.datetime(1988, 7, 7, 0, 0, 0, 0)
    is_dob_estimated = NO
    gender = "F"
    citizen = YES
    identity = "111121111"
    identity_type = "OMANG"
    confirm_identity = "111121111"
    consent_reviewed = YES
    study_questions = YES
    is_literate = YES
    assessment_score = YES
    consent_signature = YES
    consent_copy = YES
    language = settings.LANGUAGES
