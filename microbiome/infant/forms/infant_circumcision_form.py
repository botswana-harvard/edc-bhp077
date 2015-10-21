from ..models import InfantCircumcision

from .base_infant_model_form import BaseInfantModelForm


class InfantCircumcisionForm(BaseInfantModelForm):

    class Meta:
        model = InfantCircumcision
        fields = '__all__'
