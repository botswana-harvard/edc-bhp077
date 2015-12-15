from django import forms

from edc_constants.constants import YES, NOT_APPLICABLE

from bhp077.apps.microbiome_infant.constants import REALTIME

from ..constants import BROUGHT
from ..models import InfantStoolCollection

from .base_infant_model_form import BaseInfantModelForm


class InfantStoolCollectionForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(InfantStoolCollectionForm, self).clean()
        if cleaned_data.get('infant_visit').appointment.visit_definition.code == '2000':
            self.validate_collection_time()
            self.validate_sample_obtained()
        else:
            self.validate_sample_obtained()
            self.validate_collection_time()
            self.validate_diarrhea()
            self.validate_antibiotics()
        return cleaned_data

    def clean_infant_visit(self):
        infant_visit = self.cleaned_data['infant_visit']
        if not infant_visit:
            raise forms.ValidationError('Infant visit cannot be blank.')
        return infant_visit

    def validate_sample_obtained(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('sample_obtained') == YES:
            if cleaned_data.get('nappy_type') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'Sample is indicated to have been obtained today, Nappy type CANNOT '
                    'be Not Applicable. Please correct.')
            if cleaned_data.get('stool_collection') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'Sample is indicated to have been obtained today, collection time CANNOT '
                    'be not Applicable.')
            if (cleaned_data.get('stool_stored') == NOT_APPLICABLE and
                    cleaned_data.get('stool_collection') != REALTIME):
                raise forms.ValidationError(
                    'Sample is stated to have been obtained today, please indicate how the '
                    'sample was stored.')
        else:
            if cleaned_data.get('nappy_type') != NOT_APPLICABLE:
                raise forms.ValidationError('Sample is indicated to have NOT been collected, you CANNOT '
                                            'specify the nappy type. Please correct.')
            if cleaned_data.get('stool_collection') != NOT_APPLICABLE:
                raise forms.ValidationError(
                    'Sample is indicated to have NOT been obtained today, you cannot specify '
                    'the collection time. Please correct.')
            if cleaned_data.get('stool_stored') != NOT_APPLICABLE:
                raise forms.ValidationError(
                    'Sample is stated to have been NOT obtained today, you cannot specify how '
                    'the sample was stored.')

    def validate_collection_time(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('stool_collection') == BROUGHT:
            if not cleaned_data.get('stool_collection_time'):
                raise forms.ValidationError('Please specify the number of hours that stool was collected.')
        else:
            if cleaned_data.get('stool_collection_time'):
                raise forms.ValidationError(
                    'You have stated that stool was collected real-time. You cannot indicate '
                    'the number of hour ago the stool was collected.')
            if cleaned_data.get('stool_stored') != NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You have indicated that stool was collected real-time. How tool was stored '
                    'should be NOT APPLICABLE.')

    def validate_diarrhea(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('sample_obtained') == YES:
            if cleaned_data.get('past_diarrhea') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'Sample is indicated to have been obtained. Did the child have diarrhea?')
        if cleaned_data.get('past_diarrhea') == YES:
            if cleaned_data.get('diarrhea_past_24hrs') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You have indicated the infant had diarrhea in the past 7 days, please '
                    'indicate if occurred in the past 24 hours.')
        else:
            if cleaned_data.get('diarrhea_past_24hrs') != NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You have stated the infant did NOT have diarrhea in the past 7 days, '
                    'you cannot indicate if it occurred in the past 24 hours.')

    def validate_antibiotics(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('sample_obtained') == YES:
            if cleaned_data.get('antibiotics_7days') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'Sample is indicated to have been obtained. Did the child take antibiotics?')
        if cleaned_data.get('antibiotics_7days') == YES:
            if cleaned_data.get('antibiotic_dose_24hrs') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You have indicated the infant took antibiotics in the past 7 days, please '
                    'indicate if taken in the past 24 hours.')
        else:
            if cleaned_data.get('antibiotic_dose_24hrs') != NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You have stated the infant did NOT take antibiotics in the past 7 days, '
                    'you cannot indicate antibiotics were taken in the past 24 hours.')

    class Meta:
        model = InfantStoolCollection
        fields = '__all__'
