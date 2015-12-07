from django import forms

from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalBreastHealth
from edc_constants.constants import YES, NOT_APPLICABLE, NO


class MaternalBreastHealthForm(BaseMaternalModelForm):
    def clean(self):
        cleaned_data = super(MaternalBreastHealthForm, self).clean()
        self.validate_breast_feeding()
        self.validate_mastitis()
        self.validate_lesions()
        self.validate_to_stop_bf()
        return cleaned_data

    def validate_breast_feeding(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('breast_feeding') == YES:
            if cleaned_data.get('has_mastitis') == NOT_APPLICABLE:
                raise forms.ValidationError('You indicated that the mother has been breastfeeding. '
                                            'Has mastitis CANNOT be Not Applicable.')
            if cleaned_data.get('has_lesions') == NOT_APPLICABLE:
                raise forms.ValidationError('You indicated that the mother has been breastfeeding. '
                                            'Has lesions CANNOT be Not Applicable.')

    def validate_mastitis(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('has_mastitis') == YES:
            if cleaned_data.get('mastitis') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You indicated the mother has mastitis. You cannot answer Not applicable'
                    ' to indicate where.')
        else:
            if cleaned_data.get('mastitis') != NOT_APPLICABLE:
                raise forms.ValidationError('You stated that mother did not have mastitis, yet indicated '
                                            'where mother if affected. Please correct.')

    def validate_lesions(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('has_lesions') == YES:
            if cleaned_data.get('lesions') == NOT_APPLICABLE:
                raise forms.ValidationError('You stated that mother has lesions. Please indicate where.')
        else:
                if cleaned_data.get('lesions') != NOT_APPLICABLE:
                    raise forms.ValidationError(
                        'You stated that mother does not have lesions, yet indicated where she '
                        'has lesions. Please correct')

    def validate_to_stop_bf(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('has_mastitis') == YES or cleaned_data.get('has_lesions') == YES:
            if cleaned_data.get('advised_stop_bf') == NOT_APPLICABLE:
                raise forms.ValidationError('You indicated that participant has mastitis or has lesions. Was '
                                            'participant advised to stop breast feeding CANNOT be Not Applicable.')
        if cleaned_data.get('breast_feeding') == NO and cleaned_data.get('advised_stop_bf') != NOT_APPLICABLE:
            raise forms.ValidationError('You indicated that the mother has not been breast feeding, question on whether'
                                        ' she was advised to stop breast feeding should be Not Applicable.')

    class Meta:
        model = MaternalBreastHealth
        fields = '__all__'
