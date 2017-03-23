from django import forms

from edc_constants.constants import YES, NO, NOT_APPLICABLE

from .base_infant_model_form import BaseInfantModelForm
from ..models import InfantFeeding


class InfantFeedingForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(InfantFeedingForm, self).clean()
        self.validate_other_feeding()
        self.validate_formula_intro_occur(cleaned_data)
        self.validate_took_formula()
        self.validate_cows_milk()
        return cleaned_data

    def validate_other_feeding(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('other_feeding') == YES:
            answer = False
            for question in ['juice', 'cow_milk', 'other_milk', 'fruits_veg',
                             'cereal_porridge', 'solid_liquid']:
                if cleaned_data.get(question) == YES:
                    answer = True
                    break
            if not answer:
                raise forms.ValidationError(
                    'You should answer YES either on juice, cow_milk, '
                    'other_milk, fruits_veg, cereal_porridge or '
                    'solid_liquid.')
            if cleaned_data.get('formula_intro_occur') in NOT_APPLICABLE:
                raise forms.ValidationError(
                    'Last attended visit (Q3) is Yes, introduction of formula '
                    'or other foods or liquids (Q4) should be YES or NO.')
        else:
            if cleaned_data.get('formula_intro_date') or cleaned_data.get('other_feeding') not in NOT_APPLICABLE:
                        raise forms.ValidationError(
                            'You mentioned no formula milk | foods | liquids received'
                            ' since last visit. DO NOT PROVIDE DATE')

    def validate_took_formula(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('took_formula') == YES:
            if not cleaned_data.get('is_first_formula'):
                raise forms.ValidationError(
                    'Infant took formula, is this the first reporting of infant formula use?')
        else:
            if cleaned_data.get('is_first_formula'):
                raise forms.ValidationError('You mentioned that infant did not take formula,'
                                            ' PLEASE DO NOT PROVIDE FIRST FORMULA USE INFO')

        if cleaned_data.get('is_first_formula') == YES:
            if not cleaned_data.get('date_first_formula') and not cleaned_data.get('est_date_first_formula'):
                raise forms.ValidationError('If this is a first reporting of infant formula'
                                            ' please provide date and if date is estimated')
        else:
            if cleaned_data.get('date_first_formula') and cleaned_data.get('est_date_first_formula'):
                raise forms.ValidationError('You mentioned that is not the first reporting of infant formula'
                                            ' PLEASE DO NOT PROVIDE DATE AND EST DATE')

    def validate_cows_milk(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('cow_milk') == YES:
            if cleaned_data.get('cow_milk_yes') == 'N/A':
                raise forms.ValidationError('If infant took cows milk. Answer CANNOT be Not Applicable')
        else:
            if not cleaned_data.get('cow_milk_yes') == 'N/A':
                raise forms.ValidationError('Infant did not take cows milk. Answer is NOT APPLICABLE')

    def validate_formula_intro_occur(self, cleaned_data):
            infant_identifier = cleaned_data.get('infant_visit').subject_identifier
            previous_feeding_date = self.get_previous_feeding(infant_identifier)
            current_visit_code = cleaned_data.get('infant_visit').appointment.visit_definition.code
            if current_visit_code not in ['2030']:
                if cleaned_data.get('formula_intro_occur') == YES:
                    if not previous_feeding_date:
                        raise forms.ValidationError(
                            'There is no previous feeding with a formula introduction '
                            'date, formula introduction should be NO and provide a '
                            'formula introduction date.')
                if cleaned_data.get('formula_intro_occur') == NO:
                    if previous_feeding_date and cleaned_data.get('formula_intro_date'):
                        raise forms.ValidationError(
                            'Infant has a previous date of formula milk | foods | liquids of {}, '
                            'no need to give this date again.'.format(previous_feeding_date))
                    if not cleaned_data.get('formula_intro_date'):
                        raise forms.ValidationError(
                            'If received formula milk | foods | liquids since last'
                            ' attended visit. Please provide intro date')

    def get_previous_feeding(self, infant_identifier):
        """Return a previous infant feeding object if there was a previous formula or other liquid date filled."""
        infant_feedings = InfantFeeding.objects.filter(
            infant_visit__subject_identifier=infant_identifier).order_by('-report_datetime')
        for infant_feeding in infant_feedings:
            if infant_feeding.formula_intro_date:
                return infant_feeding.formula_intro_date
        return None

    class Meta:
        model = InfantFeeding
        fields = '__all__'
