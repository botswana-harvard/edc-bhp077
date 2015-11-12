from django import forms

from base_maternal_model_form import BaseMaternalModelForm

from edc_constants.constants import YES, NO

from ..models import MaternalArvPreg, MaternalArv


class MaternalArvPregForm(BaseMaternalModelForm):

    def clean(self):
            cleaned_data = self.cleaned_data
            if cleaned_data.get('is_interrupt') == YES and cleaned_data.get('interrupt') == 'N/A':
                raise forms.ValidationError('You indicated that ARVs were interrupted during pregnancy. '
                                            'Please provide a reason for interruption')
            if cleaned_data.get('is_interrupt') == NO and cleaned_data.get('interrupt') != 'N/A':
                raise forms.ValidationError('You indicated that ARVs were NOT interrupted during pregnancy. '
                                            'You cannot provide a reason. Please correct.')
            return cleaned_data

    class Meta:
        model = MaternalArvPreg
        fields = '__all__'


class MaternalArvForm(BaseMaternalModelForm):

    class Meta:
        model = MaternalArv
        fields = '__all__'
