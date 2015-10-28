from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalMedicalHistory


class MaternalMedicalHistoryForm(BaseMaternalModelForm):

    class Meta:
        model = MaternalMedicalHistory
        fields = '__all__'
