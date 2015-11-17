from django import forms
from ..models import InfantFeeding

from .base_infant_model_form import BaseInfantModelForm
from edc_constants.constants import YES, NO, NOT_APPLICABLE


class InfantFeedingForm(BaseInfantModelForm):

    class Meta:
        model = InfantFeeding
        fields = '__all__'

    def clean(self):
        cleaned_data = super(InfantFeedingForm, self).clean()
        self.validate_formula_intro_occur(cleaned_data)
        self.validate_cow_milk(cleaned_data)
        self.validate_other_milk(cleaned_data)
        self.validate_ever_breastfeed(cleaned_data)
        return cleaned_data

    def validate_formula_intro_occur(self, cleaned_data):
        if cleaned_data.get('formula_intro_occur') == YES:
            if not cleaned_data.get('formula_date'):
                raise forms.ValidationError('Please, provide the date participant first received formula milk.')
            answer = False
            for question in [
            'juice', 'cow_milk', 'boiled', 'other_milk', 'fruits_veg', 'cereal_porridge', 'solid_liquid']:
                if cleaned_data.get(question) == YES:
                    answer = True
                    break
            if not answer:
                raise forms.ValidationError(
                    'You should answer (yes) either on Q9, Q10, Q11, Q12, Q15, Q16 or Q17.')

    def validate_cow_milk(self, cleaned_data):
        if cleaned_data.get('cow_milk') == YES:
            if not cleaned_data.get('cow_milk_yes') == NOT_APPLICABLE:
                raise forms.ValidationError('Please, provide answer for Q11.')
        else:
            if cleaned_data.get('cow_milk_yes') == NOT_APPLICABLE:
                raise forms.ValidationError('The answer to question 11 cannot be NOT APPLICABLE.')

    def validate_other_milk(self, cleaned_data):
        if cleaned_data.get('other_milk') == YES:
            if not cleaned_data.get('other_milk_animal'):
                raise forms.ValidationError('Please, provide answer for question 13.')
            if cleaned_data.get('milk_boiled') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'Do not select NOT APPLICABLE for question 14, if the answer to Q12 is yes.')
        else:
            if cleaned_data.get('other_milk_animal'):
                raise forms.ValidationError('Do not provide answer for question 13.')

    def validate_ever_breastfeed(self, cleaned_data):
        if cleaned_data.get('ever_breastfeed') == NO:
            if not cleaned_data.get('complete_weaning') == NOT_APPLICABLE:
                raise forms.ValidationError('Please, select NOT APPLICABLE for question 24.')
        elif cleaned_data.get('ever_breastfeed') == YES:
            if cleaned_data.get('complete_weaning') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'Please, do not select NOT APPLICABLE for question 24, select appropriate answer.')



