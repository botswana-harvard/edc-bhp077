import factory

from django.utils import timezone

from microbiome.apps.mb_infant.models import InfantCns


class InfantBirthCnsAbnItemFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantCns

    report_datetime = timezone.now()
    cns = 'Anencephaly'
