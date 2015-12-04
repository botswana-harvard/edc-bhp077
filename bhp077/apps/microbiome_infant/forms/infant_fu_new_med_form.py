from django import forms

from edc_constants.constants import OTHER, NO, YES

from ..models import InfantFuNewMed, InfantFuNewMedItems

from .base_infant_model_form import BaseInfantModelForm


class InfantFuNewMedForm(BaseInfantModelForm):
    def clean(self):
        cleaned_data = super(InfantFuNewMedForm, self).clean()
        check_items = self.data.get('infantfunewmeditems_set-0-medication')
        if cleaned_data.get('new_medications') == YES and not check_items:
            raise forms.ValidationError('You have indicated that participant took medications. Please provide them.')
        return cleaned_data

    class Meta:
        model = InfantFuNewMed
        fields = '__all__'


class InfantFuNewMedItemsForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(InfantFuNewMedItemsForm, self).clean()
        if cleaned_data.get('infant_fu_med').new_medications == NO:
            raise forms.ValidationError('You indicated that no medications were taken. You cannot provide the '
                                        'medication. Please correct')
        if cleaned_data.get('stop_date'):
            if cleaned_data.get('stop_date') < cleaned_data.get('date_first_medication'):
                raise forms.ValidationError('You have indicated that medication stop date is before its start date. '
                                            'Please correct.')
        if cleaned_data.get('medication') == OTHER and not cleaned_data.get('other_medication'):
            raise forms.ValidationError('Please specify other medication.')
        return cleaned_data

    class Meta:
        model = InfantFuNewMedItems
        fields = '__all__'
