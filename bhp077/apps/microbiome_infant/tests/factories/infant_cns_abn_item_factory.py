import factory

from django.utils import timezone

from bhp077.apps.microbiome_infant.models import InfantCns


class InfantBirthCnsAbnItemFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantCns

    report_datetime = timezone.now()
    cns = 'Anencephaly'
