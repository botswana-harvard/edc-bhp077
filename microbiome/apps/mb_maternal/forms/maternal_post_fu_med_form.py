from django import forms

from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalPostFuMed, MaternalPostFuMedItems
from edc_constants.constants import NO, YES


class MaternalPostFuMedForm(BaseMaternalModelForm):
    def clean(self):
        cleaned_data = super(MaternalPostFuMedForm, self).clean()
        check_med_items = self.data.get('maternalpostfumeditems_set-0-medication')
        if cleaned_data.get('has_taken_meds') == YES and not check_med_items:
            raise forms.ValidationError(
                'You have indicated that medications were taken. Please provide them')
        return cleaned_data

    class Meta:
        model = MaternalPostFuMed
        fields = '__all__'


class MaternalPostFuMedItemsForm(BaseMaternalModelForm):
    def clean(self):
        cleaned_data = super(MaternalPostFuMedItemsForm, self).clean()
        if cleaned_data.get('maternal_post_fu_med').has_taken_meds in ['Unknown', NO]:
            raise forms.ValidationError(
                'You indicated that has taken meds was {} therefore you cannot provide '
                'medication. Please correct.'.format(
                    cleaned_data.get('maternal_post_fu_med').has_taken_meds))
        if cleaned_data.get('date_stoped'):
            if cleaned_data.get('date_stoped') < cleaned_data.get('date_first_medication'):
                raise forms.ValidationError(
                    'Date stopped medication is before date started medications. Please correct')
        return cleaned_data

    class Meta:
        model = MaternalPostFuMedItems
        fields = '__all__'
