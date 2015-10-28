from ..models import InfantBirthExam

from .base_infant_model_form import BaseInfantModelForm


class InfantBirthExamForm(BaseInfantModelForm):

    class Meta:
        model = InfantBirthExam
        fields = '__all__'
