from django import forms

from edc.lab.lab_requisition.forms import BaseRequisitionForm
from edc_constants.constants import YES, NO, SCHEDULED, UNSCHEDULED

from ..models import InfantRequisition
from bhp077.apps.microbiome_infant.models import InfantStoolCollection, InfantVisit


class InfantRequisitionForm(BaseRequisitionForm):

    def __init__(self, *args, **kwargs):
        super(InfantRequisitionForm, self).__init__(*args, **kwargs)
        self.fields['item_type'].initial = 'tube'

    def clean(self):
        cleaned_data = super(InfantRequisitionForm, self).clean()
        self.validate_requisition_and_drawn_datetime()
        self.validate_sample_swabs()
        self.validate_dna_pcr_and_elisa()
        self.validate_stool_sample_collection()
        self.validate_requisition_and_infant_visit()
        return cleaned_data

    def validate_requisition_and_drawn_datetime(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('drawn_datetime'):
            if cleaned_data.get('drawn_datetime').date() < cleaned_data.get('requisition_datetime').date():
                raise forms.ValidationError('Requisition date cannot be in future of specimen date. Specimen draw date is '
                                            'indicated as {}, whilst requisition is indicated as{}. Please correct'
                                            .format(cleaned_data.get('drawn_datetime').date(),
                                                    cleaned_data.get('requisition_datetime').date()))

    def validate_sample_swabs(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('panel').name == 'Rectal swab (Storage)':
            if cleaned_data.get('item_type') != 'swab':
                raise forms.ValidationError('Panel {} is a swab therefore collection type is swab. Please correct.'
                                            .format(cleaned_data.get('panel').name))

    def validate_dna_pcr_and_elisa(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('panel').name in ['DNA PCR', 'ELISA']:
            if cleaned_data.get('item_type') not in ['dbs', 'tube']:
                raise forms.ValidationError('Panel {} collection type can only be dbs or tube. '
                                            'Please correct.'.format(cleaned_data.get('panel').name))

    def validate_stool_sample_collection(self):
        cleaned_data = self.cleaned_data
        sample_collection = InfantStoolCollection.objects.filter(infant_visit=cleaned_data.get('infant_visit'))
        if sample_collection:
            sample_collection = InfantStoolCollection.objects.get(infant_visit=cleaned_data.get('infant_visit'))
            if sample_collection.sample_obtained == YES:
                if (cleaned_data.get("panel").name == 'Stool storage' and cleaned_data.get("is_drawn") == NO):
                    raise forms.ValidationError("Stool Sample Collected. Stool Requisition is_drawn"
                                                " cannot be NO.")

    def validate_requisition_and_infant_visit(self):
        cleaned_data = self.cleaned_data
        infant_visit = InfantVisit.objects.get(
            appointment__registered_subject=cleaned_data.get('infant_visit').appointment.registered_subject,
            appointment=cleaned_data.get('infant_visit').appointment,
            appointment__visit_instance=cleaned_data.get('infant_visit').appointment.visit_instance)
        if infant_visit:
            if ((infant_visit.reason == SCHEDULED or infant_visit.reason == UNSCHEDULED) and
                    cleaned_data.get('reason_not_drawn') == 'absent'):
                raise forms.ValidationError(
                    'Reason not drawn cannot be {}. The infant visit report reason is {}'.format(
                        cleaned_data.get('reason_not_drawn'),
                        infant_visit.reason))

    class Meta:
        model = InfantRequisition
