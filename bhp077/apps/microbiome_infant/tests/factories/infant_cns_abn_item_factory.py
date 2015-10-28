import factory

from django.utils import timezone

from ...infant.models import InfantCnsAbnormalityItems


class InfantBirthCnsAbnItemFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantCnsAbnormalityItems

    report_datetime = timezone.now()
    cns_abnormality = 'Anencephaly'
