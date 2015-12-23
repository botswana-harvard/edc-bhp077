import factory

from django.utils import timezone

from microbiome.apps.mb_infant.models import InfantBirth

from microbiome.apps.mb_maternal.tests.factories.maternal_labour_del_factory import MaternalLabourDelFactory


class InfantBirthFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantBirth

    report_datetime = timezone.now()
    maternal_labour_del = factory.SubFactory(MaternalLabourDelFactory)
    first_name = 'BABY'
    initials = 'BB'
    dob = timezone.now().date()
    gender = 'F'
