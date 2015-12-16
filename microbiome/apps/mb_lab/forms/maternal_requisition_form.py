from django import forms

from edc.lab.lab_requisition.forms import BaseRequisitionForm
from edc_constants.constants import SCHEDULED, UNSCHEDULED

from ..models import MaternalRequisition
from microbiome.apps.mb_maternal.models import MaternalVisit


class MaternalRequisitionForm(BaseRequisitionForm):

    def __init__(self, *args, **kwargs):
        super(MaternalRequisitionForm, self).__init__(*args, **kwargs)
        self.fields['item_type'].initial = 'tube'
        self.fields['requisition_identifier'].required = False

    def clean(self):
        cleaned_data = super(MaternalRequisitionForm, self).clean()
        if cleaned_data.get('drawn_datetime'):
            if cleaned_data.get('drawn_datetime').date() < cleaned_data.get('requisition_datetime').date():
                raise forms.ValidationError(
                    'Requisition date cannot be in future of specimen date. Specimen draw date is '
                    'indicated as {}, whilst requisition is indicated as{}. Please correct'.format(
                        cleaned_data.get('drawn_datetime').date(),
                        cleaned_data.get('requisition_datetime').date()))
        if (
            cleaned_data.get('panel').name == 'Vaginal swab (Storage)' or
            cleaned_data.get('panel').name == 'Rectal swab (Storage)' or
            cleaned_data.get('panel').name == 'Skin Swab (Storage)' or
            cleaned_data.get('panel').name == 'Vaginal Swab (multiplex PCR)'
        ):
            if cleaned_data.get('item_type') != 'swab':
                raise forms.ValidationError('Panel is a swab therefore collection type is swab. Please correct.')
        else:
            if cleaned_data.get('item_type') != 'tube':
                raise forms.ValidationError('Panel {} can only be tube therefore collection type is swab. '
                                            'Please correct.'.format(cleaned_data.get('panel').name))
        maternal_visit = MaternalVisit.objects.get(
            appointment__registered_subject=cleaned_data.get('maternal_visit').appointment.registered_subject,
            appointment=cleaned_data.get('maternal_visit').appointment,
            appointment__visit_instance=cleaned_data.get('maternal_visit').appointment.visit_instance)
        if maternal_visit:
            if ((maternal_visit.reason == SCHEDULED or maternal_visit.reason == UNSCHEDULED) and
                    cleaned_data.get('reason_not_drawn') == 'absent'):
                raise forms.ValidationError(
                    'Reason not drawn cannot be {}. Visit report reason is {}'.format(
                        cleaned_data.get('reason_not_drawn'),
                        maternal_visit.reason))
        return cleaned_data

    class Meta:
        model = MaternalRequisition
        fields = '__all__'
