import factory

from django.utils import timezone

from edc_constants.constants import YES, NO
from edc.subject.registration.tests.factories import RegisteredSubjectFactory

from bhp077.apps.microbiome_maternal.models import MaternalOffStudy
from bhp077.apps.microbiome_maternal.tests.factories import MaternalVisitFactory


class MaternalOffStudyFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalOffStudy

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)

    offstudy_date = timezone.now().date()

    maternal_visit = factory.SubFactory(MaternalVisitFactory)
