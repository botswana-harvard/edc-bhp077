from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalMedicalHistory


class MaternalMedicalHistoryForm(BaseMaternalModelForm):

    class Meta:
        model = MaternalMedicalHistory
        fields = '__all__'

    def clean(self):
        cleaned_data = super(MaternalMedicalHistoryForm, self).clean()
        if 'chronic_cond' in cleaned_data.keys():
            self.validate_m2m(
                label='chronic condition',
                leading=cleaned_data.get('has_chronic_cond'),
                m2m=cleaned_data.get('chronic_cond'),
                other=cleaned_data.get('chronic_cond_other'))
        # WHO validations
        if 'wcs_dx_adult' in cleaned_data.keys():
            self.validate_m2m_wcs_dx(
                label='WHO diagnoses',
                leading=cleaned_data.get('who_diagnosis'),
                m2m=cleaned_data.get('wcs_dx_adult'))

        return cleaned_data
