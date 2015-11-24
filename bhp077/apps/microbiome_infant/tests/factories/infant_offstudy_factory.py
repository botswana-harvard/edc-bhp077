import factory

from django.utils import timezone

from edc.subject.registration.tests.factories import RegisteredSubjectFactory

from bhp077.apps.microbiome_infant.models import InfantOffStudy

from .infant_visit_factory import InfantVisitFactory


class InfantOffStudyFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantOffStudy

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)

    offstudy_date = timezone.now().date()

    infant_visit = factory.SubFactory(InfantVisitFactory)
