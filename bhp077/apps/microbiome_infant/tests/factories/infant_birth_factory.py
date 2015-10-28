import factory

from django.utils import timezone

from ...infant.models import InfantBirth

from .maternal_labour_del_factory import MaternalLabourDelFactory


class InfantBirthFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantBirth

    maternal_labour_del = factory.SubFactory(MaternalLabourDelFactory)
    first_name = factory.Sequence(lambda n: 'RANGO{0}'.format(n))
    initials = factory.Sequence(lambda n: 'R{0}'.format(n))
    birth_order = 1
    dob = timezone.now().date()
    gender = 'F'
