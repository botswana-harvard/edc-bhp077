import factory

from django.utils import timezone

from microbiome.apps.mb_infant.models import InfantFuPhysical

from edc_constants.constants import YES


class InfantFuPhysicalFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantFuPhysical

    report_datetime = timezone.now()
    weight_kg = 3
    head_circumference = 18
    general_activity = "NORMAL"
    physical_exam_result = "NORMAL"
    heent_exam = YES
    was_hospitalized = YES
