from ..models import InfantVisit

from .base_infant_model_form import BaseInfantModelForm


class InfantVisitForm(BaseInfantModelForm):

    class Meta:
        model = InfantVisit
        fields = '__all__'
