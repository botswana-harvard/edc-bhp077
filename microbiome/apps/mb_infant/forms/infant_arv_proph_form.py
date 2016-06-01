from django import forms
from django.forms.models import ModelForm

from edc_constants.constants import NO, YES


from microbiome.apps.mb.constants import MODIFIED, DISCONTINUED, NEVER_STARTED

from edc_constants.constants import UNKNOWN

from ..models import InfantArvProph, InfantArvProphMod, InfantBirthArv, InfantVisit

from .base_infant_model_form import BaseInfantModelForm


class InfantArvProphForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        self.validate_taking_arv_proph_no()
        self.validate_taking_arv_proph_yes()
        return cleaned_data

    def validate_taking_arv_proph_no(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('prophylatic_nvp') == NO:
            infant_identifier = cleaned_data.get('infant_visit').subject_identifier
            if cleaned_data.get('arv_status') not in [NEVER_STARTED, DISCONTINUED]:
                raise forms.ValidationError(
                    'Infant was not taking prophylactic arv, prophylaxis should be Never Started or Discontinued.')
            if cleaned_data.get('arv_status') == DISCONTINUED and self.get_birth_arv_status_visit_2000(infant_identifier):
                    raise forms.ValidationError(
                        'The azt after birth in Infant birth arv was answered as NO or Unknown,'
                        'therefore Infant ARV proph in this visit cannot be permanently discontinued.')

    def validate_taking_arv_proph_yes(self):
        cleaned_data = self.cleaned_data
        if (cleaned_data.get('prophylatic_nvp') == YES and
           cleaned_data.get('arv_status') in [NEVER_STARTED, DISCONTINUED]):
            raise forms.ValidationError(
                'Infant has been on prophylactic arv, cannot choose Never Started or Permanently discontinued.')

    def get_birth_arv_status_visit_2000(self, infant_identifier):
        """Check if infant was given AZT at birth"""
        try:
            visit_2000 = InfantVisit.objects.get(subject_identifier=infant_identifier, appointment__visit_definition__code=2000)
            infant_birth_arv = InfantBirthArv.objects.get(infant_visit=visit_2000)
            if infant_birth_arv.azt_after_birth in [NO, UNKNOWN]:
                return True
        except:
            pass
        return False

    class Meta:
        model = InfantArvProph
        fields = '__all__'


class InfantArvProphModForm(ModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        self.validate_proph_mod_fields()
        self.validate_infant_arv_proph_not_modified()
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

    def validate_infant_arv_proph_not_modified(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('infant_arv_proph').arv_status != MODIFIED:
            raise forms.ValidationError("You did NOT indicate that medication was modified, so do not ENTER "
                                        "arv inline.")

    class Meta:
        model = InfantArvProphMod
        fields = '__all__'
