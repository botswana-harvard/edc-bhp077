from bhp077.apps.microbiome.base_model_form import BaseModelForm

from ..models import PostnatalCallList


class PostnatalCallListForm (BaseModelForm):

    class Meta:
        model = PostnatalCallList
