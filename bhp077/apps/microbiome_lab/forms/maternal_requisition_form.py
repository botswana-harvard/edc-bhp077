from django import forms

from edc.lab.lab_requisition.forms import BaseRequisitionForm

from ..models import MaternalRequisition


class MaternalRequisitionForm(BaseRequisitionForm):

    def __init__(self, *args, **kwargs):
        super(MaternalRequisitionForm, self).__init__(*args, **kwargs)
        self.fields['item_type'].initial = 'tube'

    def clean(self):
        cleaned_data = super(MaternalRequisitionForm, self).clean()
        if cleaned_data.get('drawn_datetime').date() < cleaned_data.get('requisition_datetime').date():
            raise forms.ValidationError('Requisition date cannot be in future of specimen date. Specimen draw date is '
                                        'indicated as {}, whilst requisition is indicated as{}. Please correct'
                                        .format(cleaned_data.get('drawn_datetime').date(),
                                                cleaned_data.get('requisition_datetime').date()))
        if (
            cleaned_data.get('panel').name == 'Vaginal swab (Storage)' or
            cleaned_data.get('panel').name == 'Rectal swab (Storage)' or
            cleaned_data.get('panel').name == 'Skin Swab (Storage)' or
            cleaned_data.get('panel').name == 'Vaginal Swab (multiplex PCR)'
        ):
            if cleaned_data.get('item_type') != 'swab':
                raise forms.ValidationError('Panel is a swab therefore collection type is swab. Please correct.')
        return cleaned_data

    class Meta:
        model = MaternalRequisition
        fields = '__all__'
