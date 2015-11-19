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

        return cleaned_data
