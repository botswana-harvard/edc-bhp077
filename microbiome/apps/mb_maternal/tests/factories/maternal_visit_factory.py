import factory
from django.utils import timezone

from edc.subject.appointment.tests.factories import AppointmentFactory

from microbiome.apps.mb_maternal.models import MaternalVisit


class MaternalVisitFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalVisit

    report_datetime = timezone.now()
    appointment = factory.SubFactory(AppointmentFactory)
    reason = "scheduled"
    info_source = "participant"
