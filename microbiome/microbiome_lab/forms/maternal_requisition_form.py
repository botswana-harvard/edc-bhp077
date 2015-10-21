from edc.lab.lab_requisition.forms import BaseRequisitionForm

from ..models import MaternalRequisition


class MaternalRequisitionForm(BaseRequisitionForm):

    def __init__(self, *args, **kwargs):
        super(MaternalRequisitionForm, self).__init__(*args, **kwargs)
        self.fields['item_type'].initial = 'tube'

    class Meta:
        model = MaternalRequisition
