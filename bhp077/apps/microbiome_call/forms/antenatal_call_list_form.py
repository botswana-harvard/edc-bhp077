from bhp077.apps.microbiome.base_model_form import BaseModelForm

from ..models import AntenatalCallList


class AntenatalCallListForm (BaseModelForm):

    class Meta:
        model = AntenatalCallList
