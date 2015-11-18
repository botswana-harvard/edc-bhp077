from django import forms

from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalPostFu, MaternalPostFuDx, MaternalPostFuDxT
from edc_constants.constants import NO


class MaternalPostFuForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('systolic_bp') < cleaned_data.get('diastolic_bp'):
            forms.ValidationError('Systolic blood pressure can never be less than diastolic blood pressure, please check and correct.')
        if cleaned_data.get('systolic_bp') < 75 or cleaned_data.get('systolic_bp') > 175:
            forms.ValidationError('Systolic blood pressure should be between 75 and 175, please check and correct.')
        if cleaned_data.get('diastolic_bp') < 35 or cleaned_data.get('diastolic_bp') > 130:
            forms.ValidationError('Diastolic blood pressure should be between 35 and 130, please check and correct.')
        return super(MaternalPostFuForm, self).clean()

    class Meta:
        model = MaternalPostFu
        fields = '__all__'


class MaternalPostFuDxForm(BaseMaternalModelForm):

    class Meta:
        model = MaternalPostFuDx
        fields = '__all__'


class MaternalPostFuDxTForm (BaseMaternalModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('maternal_post_fu').new_diagnoses == NO and cleaned_data.get('post_fu_dx'):
            raise forms.ValidationError('You indicated that there was NO new diagnosis'
                                        ' and yet provided a diagnosis. Please correct.')

        if cleaned_data.get('post_fu_dx'):
            if not cleaned_data.get('post_fu_specify') or not cleaned_data.get('grade') or not cleaned_data.get('hospitalized'):
                raise forms.ValidationError('Please fill in all diagnosis information.')

        if cleaned_data.get('maternal_post_fu').mother_hospitalized == NO and cleaned_data.get('hospitalized'):
            raise forms.ValidationError('You indicated that participant was not hospitalized above. Please correct.')

        return super(MaternalPostFuDxTForm, self).clean()

    class Meta:
        model = MaternalPostFuDxT
        fields = '__all__'
