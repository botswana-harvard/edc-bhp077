import factory

from django.utils import timezone

from bhp077.apps.microbiome_infant.models import InfantCnsAbnormalityItems


class InfantBirthCnsAbnItemFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantCnsAbnormalityItems

    report_datetime = timezone.now()
    cns_abnormality = 'Anencephaly'
