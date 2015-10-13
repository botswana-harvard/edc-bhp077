from lis.specimen.lab_aliquot_list.models import BaseAliquotType
from lis.specimen.lab_aliquot_list.managers import AliquotTypeManager


class AliquotType(BaseAliquotType):

    objects = AliquotTypeManager()

    class Meta:
        app_label = 'lab'
        ordering = ["name"]
