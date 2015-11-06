import factory
from django.utils import timezone

from edc.subject.appointment.tests.factories import AppointmentFactory

from bhp077.apps.microbiome_maternal.models import MaternalVisit


class MaternalVisitFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalVisit

    report_datetime = timezone.now()
    appointment = factory.SubFactory(AppointmentFactory)
    reason = "NA"
#    info_source = ""
#    subject_identifier = ""
