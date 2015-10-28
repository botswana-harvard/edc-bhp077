from ..models import MaternalArvHistory
from base_maternal_model_form import BaseMaternalModelForm


class MaternalArvHistoryForm(BaseMaternalModelForm):

    class Meta:
        model = MaternalArvHistory
        fields = '__all__'
