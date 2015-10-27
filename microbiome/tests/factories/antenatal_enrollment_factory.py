import factory

from datetime import datetime

from edc_registration.tests.factories import RegisteredSubjectFactory

from ...maternal.models import AntenatalEnrollment


class AntenatalEnrollmentFactory(factory.DjangoModelFactory):

    class Meta:
        model = AntenatalEnrollment

    weeks_of_gestation = 32
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    report_datetime = datetime.today()
