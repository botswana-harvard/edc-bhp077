from django import forms

from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalClinicalHistory


class MaternalClinicalHistoryForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalClinicalHistoryForm, self).clean()
        if cleaned_data.get('lowest_cd4_known') == 'Yes' and not cleaned_data.get('cd4_count') and not cleaned_data.get('cd4_date') and not cleaned_data.get('is_date_estimated'):
            raise forms.ValidationError('If the lowest CD4 count is known, please specify the CD4 cell count, the CD4 date and whether the date is estimated or not.')

    class Meta:
        model = MaternalClinicalHistory
        fields = '__all__'
