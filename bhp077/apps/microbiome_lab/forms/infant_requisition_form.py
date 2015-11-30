from django import forms

from edc.lab.lab_requisition.forms import BaseRequisitionForm

from ..models import InfantRequisition


class InfantRequisitionForm(BaseRequisitionForm):

    def __init__(self, *args, **kwargs):
        super(InfantRequisitionForm, self).__init__(*args, **kwargs)
        self.fields['item_type'].initial = 'tube'

    def clean(self):
        cleaned_data = super(InfantRequisitionForm, self).clean()
        if cleaned_data.get('drawn_datetime').date() < cleaned_data.get('requisition_datetime').date():
            raise forms.ValidationError('Requisition date cannot be in future of specimen date. Specimen draw date is '
                                        'indicated as {}, whilst requisition is indicated as{}. Please correct'
                                        .format(cleaned_data.get('drawn_datetime').date(),
                                                cleaned_data.get('requisition_datetime').date()))
        if cleaned_data.get('panel').name == 'Rectal swab (Storage)':
            if cleaned_data.get('item_type') != 'swab':
                raise forms.ValidationError('Panel {} is a swab therefore collection type is swab. Please correct.'
                                            .format(cleaned_data.get('panel').name))
        elif (
            cleaned_data.get('panel').name == 'DNA PCR' or
            cleaned_data.get('panel').name == 'ELISA'
        ):
            if cleaned_data.get('item_type') != 'dbs' or cleaned_data.get('item_type') != 'tube':
                raise forms.ValidationError('Panel {} can only be dbs or tube therefore collection type is swab. '
                                            'Please correct.'.format(cleaned_data.get('panel').name))
        else:
            if cleaned_data.get('item_type') != 'tube':
                raise forms.ValidationError('Panel {} can only be tube therefore collection type is swab. '
                                            'Please correct.'.format(cleaned_data.get('panel').name))
        return cleaned_data

    class Meta:
        model = InfantRequisition
