from base_maternal_model_form import BaseMaternalModelForm

from ..models import MaternalObstericalHistory


class MaternalObstericalHistoryForm(BaseMaternalModelForm):

    class Meta:
        model = MaternalObstericalHistory
        fields = '__all__'
