from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalClinicalHistory


class MaternalClinicalHistoryForm(BaseMaternalModelForm):

    class Meta:
        model = MaternalClinicalHistory
        fields = '__all__'
