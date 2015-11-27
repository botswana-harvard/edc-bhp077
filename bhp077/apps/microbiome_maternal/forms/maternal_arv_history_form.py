from django import forms
from django.utils import timezone

from edc_constants.choices import YES, NO

from ..models import MaternalArvHistory
from .base_maternal_model_form import BaseMaternalModelForm


class MaternalArvHistoryForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalArvHistoryForm, self).clean()
        self.validate_arv_interrupt(cleaned_data)
        if cleaned_data.get('haart_start_date') == timezone.now().date():
            raise forms.ValidationError('tripple ARV start date CANNOT be today.')
        return cleaned_data

    def validate_arv_interrupt(self, cleaned_data):
        if cleaned_data.get(' preg_on_haart') == NO:
            if cleaned_data.get('prior_preg') == 'Received continuos HAART from the time she started':
                raise forms.ValidationError('You indicated that the mother was NOT still on tripple ARV when she '
                                            'got pregnant. There ARVs could not have been interrupted. Please correct.')
        else:
            if cleaned_data.get('prior_preg') == 'interruption never restarted':
                raise forms.ValidationError('You indicated that the mother was still on tripple ARV when '
                                            'she got pregnant, yet you indicated that ARVs were interrupted '
                                            'and never restarted.')

    class Meta:
        model = MaternalArvHistory
        fields = '__all__'
