from lis.specimen.lab_aliquot_list.managers import AliquotConditionManager
from lis.specimen.lab_aliquot_list.models import BaseAliquotCondition


class AliquotCondition(BaseAliquotCondition):

    objects = AliquotConditionManager()

    class Meta:
        app_label = 'mb_lab'
