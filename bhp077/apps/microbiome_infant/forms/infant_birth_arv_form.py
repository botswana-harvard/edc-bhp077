from django import forms

from ..models import InfantBirthArv

from edc_constants.constants import NEW, POS, YES, NO, NOT_APPLICABLE

from .base_infant_model_form import BaseInfantModelForm

from ..models import InfantBirthFeedVaccine


class InfantBirthArvForm(BaseInfantModelForm):

    class Meta:
        model = InfantBirthArv
        fields = '__all__'

    def clean(self):
        cleaned_data = super(InfantBirthArvForm, self).clean()
        self.validate_azt_after_birth(cleaned_data)
        self.validate_sdnvp_after_birth(cleaned_data)
        self.validate_nvp_discharge_supply(cleaned_data)
        return cleaned_data

    def validate_azt_after_birth(self, cleaned_data):
        if cleaned_data.get('azt_after_birth') == YES:
            if not cleaned_data.get('azt_dose_date'):
                raise forms.ValidationError('Provide date of the first dose for AZT.')
            if cleaned_data.get('azt_additional_dose') == 'N/A':
                raise forms.ValidationError('Do not select Not applicatable for Q6 if Q4 answer was yes.')

    def validate_sdnvp_after_birth(self, cleaned_data):
        if cleaned_data.get('azt_after_birth') == YES:
            if not cleaned_data.get('nvp_dose_date'):
                raise forms.ValidationError('If infant has received single dose NVP then provide NVP date.')

    def validate_nvp_discharge_supply(self, cleaned_data):
        infant_birth_feeding = InfantBirthFeedVaccine.objects.get(infant_visit=cleaned_data.get('infant_visit'))
        if infant_birth_feeding.feeding_after_delivery == 'Breastfeeding only':
            if cleaned_data.get('nvp_discharge_supply') == 'N/A':
                raise forms.ValidationError('If the infant is breast feeding then do not select not applicaticable for Q11.')
