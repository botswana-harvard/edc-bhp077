from bhp077.apps.microbiome.constants import NO_MODIFICATIONS

from ..models import InfantArvProph

from .base_infant_model_form import BaseInfantModelForm


class InfantArvProphForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        # if status is 1 or 2 or 5
        if (cleaned_data.get('arv_status', None) == NO_MODIFICATIONS or
                cleaned_data.get('arv_status', None) == 'start' or
                cleaned_data.get('arv_status', None) == 'modified'):
            raise self.forms.ValidationError("")

    class Meta:
        model = InfantArvProph
        fields = '__all__'
