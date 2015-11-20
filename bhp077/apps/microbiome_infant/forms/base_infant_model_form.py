from bhp077.apps.microbiome.base_model_form import BaseModelForm

from ..models import InfantVisit


class BaseInfantModelForm(BaseModelForm):

    visit_model = InfantVisit
