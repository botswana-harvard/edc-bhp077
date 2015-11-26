from django import forms

from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalBreastHealth
from edc_constants.constants import NO, YES, NOT_APPLICABLE


class MaternalBreastHealthForm(BaseMaternalModelForm):
    def clean(self):
        cleaned_data = super(MaternalBreastHealthForm, self).clean()
        if cleaned_data.get('breast_feeding') == YES:
            if cleaned_data.get('has_mastitis') == NOT_APPLICABLE:
                raise forms.ValidationError('You indicated that the mother has been breastfeeding. '
                                            'Has mastitis CANNOT be Not Applicable.')
        else:
            if cleaned_data.get('has_mastitis') == YES:
                raise forms.ValidationError('You indicated YES for has mother been breastfeeding. Has mastitis should '
                                            'be Not Applicable.')
        if cleaned_data.get('has_mastitis') == YES:
            if cleaned_data.get('mastitis') == NOT_APPLICABLE:
                raise forms.ValidationError('You indicated the mother has mastitis. You cannot answer Not applicable'
                                            ' to indicate where.')
        else:
            if cleaned_data.get('mastitis') != NOT_APPLICABLE:
                raise forms.ValidationError('You stated that mother did not have mastitis, yet indicated '
                                            'where mother if affected. Please correct.')
        if cleaned_data.get('has_lesions') == YES:
            if cleaned_data.get('lesions') == NOT_APPLICABLE:
                raise forms.ValidationError('You stated that mother has lesions. Please indicate where.')
        else:
                if cleaned_data.get('lesions') != NOT_APPLICABLE:
                    raise forms.ValidationError('You stated that mother does not have lesions, yet indicated where she '
                                                'has lesions. Please correct')
        return cleaned_data

    class Meta:
        model = MaternalBreastHealth
        fields = '__all__'
