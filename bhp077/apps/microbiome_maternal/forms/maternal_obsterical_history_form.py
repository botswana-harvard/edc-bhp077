from django import forms
from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalObstericalHistory


class MaternalObstericalHistoryForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('prev_pregnancies') < 0:
            raise forms.ValidationError('Number of previous pregnancies, should be greater than zero.')
        if cleaned_data.get('pregs_24wks_or_more') < 0:
            raise forms.ValidationError('Number of pregnancies at least 24 weeks, should be greater than zero.')
        else:
            if cleaned_data.get('live_children')  < 0:
                raise forms.ValidationError('How many other living children does the participant currently'
                ' have (excluding baby to be enrolled in the study.)'
                ' Provide value greater than zero.')
            if cleaned_data.get('children_died_b4_5yrs') < 0:
                raise forms.ValidationError("How many of the participant's children died after birth before 5 years of age?."
                " Provide value greater than zero.")

        if cleaned_data.get('lost_after_24wks') != cleaned_data.get('children_died_b4_5yrs') and \
                        cleaned_data.get('children_died_b4_5yrs') != cleaned_data.get('pregs_24wks_or_more'):
            raise forms.ValidationError(
                'Number of pregnancies at least 24 weeks and '
                'Number of pregnancies lost at or after 24 weeks gestation and '
                'children died after birth before 5 years of age should be the same.')
        return cleaned_data

    class Meta:
        model = MaternalObstericalHistory
        fields = '__all__'
