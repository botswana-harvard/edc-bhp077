from django import forms

from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalPostFu, MaternalPostFuDx, MaternalPostFuDxT
from edc_constants.constants import NO, YES


class MaternalPostFuForm(BaseMaternalModelForm):
    def clean(self):
        cleaned_data = super(MaternalPostFuForm, self).clean()
        if cleaned_data.get('mother_weight') == YES:
            if not cleaned_data.get('enter_weight'):
                raise forms.ValidationError('You indicated that participant was weighed. Please provide the weight.')
        else:
            if cleaned_data.get('enter_weight'):
                raise forms.ValidationError('You indicated that participant was NOT weighed, yet provided the weight. '
                                            'Please correct.')
        if 'chronic_cond' in cleaned_data.keys():
            self.validate_m2m(
                label='chronic conditions',
                leading=cleaned_data.get('has_chronic_cond'),
                m2m=cleaned_data.get('chronic_cond'),
                other=cleaned_data.get('chronic_cond_other'))
        if cleaned_data.get('systolic_bp') < cleaned_data.get('diastolic_bp'):
            raise forms.ValidationError('Systolic blood pressure cannot be lower than the diastolic blood preassure.'
                                        ' Please correct.')

    class Meta:
        model = MaternalPostFu
        fields = '__all__'


class MaternalPostFuDxForm(BaseMaternalModelForm):
    def clean(self):
        cleaned_data = super(MaternalPostFuDxForm, self).clean()
        # WHO validations
        if 'wcs_dx_adult' in cleaned_data.keys():
            self.validate_m2m_wcs_dx(
                label='who diagnoses',
                leading=cleaned_data.get('who_clinical_stage'),
                m2m=cleaned_data.get('wcs_dx_adult'))
        check_dx = self.data.get('maternalpostfudxt_set-0-post_fu_dx')
        if cleaned_data.get('new_diagnoses') == 'Yes' and not check_dx:
            raise forms.ValidationError('You indicated that participant had new diagnosis and yet did not provide '
                                        'them. Please correct.')
        return cleaned_data

    class Meta:
        model = MaternalPostFuDx
        fields = '__all__'


class MaternalPostFuDxTForm (BaseMaternalModelForm):
    def clean(self):
        cleaned_data = super(MaternalPostFuDxTForm, self).clean()

        if cleaned_data.get('maternal_post_fu').new_diagnoses == NO and cleaned_data.get('post_fu_dx'):
            raise forms.ValidationError('You indicated that there was NO new diagnosis'
                                        ' and yet provided a diagnosis. Please correct.')

        if cleaned_data.get('post_fu_dx'):
            if not (cleaned_data.get('post_fu_specify') or
                    not cleaned_data.get('grade') or
                    not cleaned_data.get('hospitalized')):
                raise forms.ValidationError('Please fill in all diagnosis information.')

        if cleaned_data.get('maternal_post_fu').mother_hospitalized == NO and cleaned_data.get('hospitalized'):
            raise forms.ValidationError('You indicated that participant was not hospitalized above. Please correct.')

        return cleaned_data

    class Meta:
        model = MaternalPostFuDxT
        fields = '__all__'
