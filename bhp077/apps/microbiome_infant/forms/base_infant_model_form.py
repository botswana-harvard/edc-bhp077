from ..models import InfantVisit
from bhp077.apps.microbiome.base_model_form import BaseModelForm


class BaseInfantModelForm(BaseModelForm):

    visit_model = InfantVisit
