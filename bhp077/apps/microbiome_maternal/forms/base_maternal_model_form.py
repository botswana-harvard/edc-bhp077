from bhp077.apps.microbiome.base_model_form import BaseModelForm
from ..models import MaternalVisit


class BaseMaternalModelForm(BaseModelForm):

    visit_model = MaternalVisit
