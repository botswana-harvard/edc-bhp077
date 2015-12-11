from django import forms
from base_maternal_model_form import BaseMaternalModelForm

from ..models import RapidTestResult

from edc_constants.constants import YES, POS, NEG, IND


class RapidTestResultForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('rapid_test_done') == YES:
            if not cleaned_data.get('rapid_test_date'):
                raise forms.ValidationError('If a rapid test was processed, what is the date'
                                            ' of the rapid test?')
            if not cleaned_data.get('result') in [POS, NEG, IND]:
                raise forms.ValidationError('If a rapid test was processed, what is the test'
                                            ' result?')
        else:
            if cleaned_data.get('rapid_test_date') or cleaned_data.get('result'):
                raise forms.ValidationError(
                    'If a rapid test was not processed, please do not provide rapid test date '
                    'and result.')
        cleaned_data = super(RapidTestResultForm, self).clean()
        return cleaned_data

    class Meta:
        model = RapidTestResult
        fields = '__all__'
