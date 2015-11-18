from django import forms

from edc_constants.constants import YES
from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalClinicalHistory


class MaternalClinicalHistoryForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('lowest_cd4_known') == YES:
            if not cleaned_data.get('cd4_count'):
                raise forms.ValidationError("If CD4 lowest count is known, what is the count?")
            if not cleaned_data.get('cd4_date'):
                raise forms.ValidationError("CD4 count is known please provide the date")
            if cleaned_data.get('cd4_date'):
                if not cleaned_data.get('is_date_estimated'):
                    raise forms.ValidationError('You have provided the CD4 date, is this estimated?')
        else:
            if cleaned_data.get('cd4_count'):
                raise forms.ValidationError("CD4 is NOT KNOWN. Do not give the count")
            if cleaned_data.get('cd4_date'):
                raise forms.ValidationError("CD4 is NOT KNOWN. Do not give the date")
            if cleaned_data.get('is_date_estimated'):
                raise forms.ValidationError("CD4 is NOT KNOWN. Do not give the date-estimated")
        return super(MaternalClinicalHistoryForm, self).clean()

    class Meta:
        model = MaternalClinicalHistory
        fields = '__all__'
