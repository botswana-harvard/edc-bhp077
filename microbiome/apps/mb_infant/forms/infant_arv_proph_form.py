from django import forms
from django.forms.models import ModelForm

from edc_constants.constants import NO, NOT_APPLICABLE

from microbiome.apps.mb.constants import NO_MODIFICATIONS

from ..models import InfantArvProph, InfantArvProphMod

from .base_infant_model_form import BaseInfantModelForm


class InfantArvProphForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        self.validate_taking_arv_proph_no()
        self.validate_infant_arv_proph_mod()
        return cleaned_data

    def validate_taking_arv_proph_no(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('prophylatic_nvp') == NO and cleaned_data.get('arv_status') not in NOT_APPLICABLE:
            raise forms.ValidationError('Infant was not taking prophylactic arv, prophylaxis should be Not Applicable.')

    def validate_infant_arv_proph_mod(self):
        cleaned_data = self.cleaned_data
        arv_proph_mods_table = self.data.get('infantarvprophmod_set-0-arv_code')
        if cleaned_data.get('arv_status') == 'modified':
            if not arv_proph_mods_table:
                raise forms.ValidationError("You indicated that the infant arv was modified, please "
                                            "give a valid Arv Code")

    class Meta:
        model = InfantArvProph
        fields = '__all__'


class InfantArvProphModForm(ModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        self.validate_proph_mod_fields()
        return cleaned_data

    def validate_proph_mod_fields(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('arv_code'):
            if not cleaned_data.get('dose_status'):
                raise forms.ValidationError('You entered an ARV Code, please give the dose status.')

            if not cleaned_data.get('modification_date'):
                raise forms.ValidationError('You entered an ARV Code, please give the modification date.')

            if not cleaned_data.get('modification_code'):
                raise forms.ValidationError('You entered an ARV Code, please give the modification reason.')

    class Meta:
        model = InfantArvProphMod
        fields = '__all__'
