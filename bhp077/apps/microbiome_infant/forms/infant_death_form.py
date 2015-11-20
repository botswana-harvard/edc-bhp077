from ..models import InfantDeath, InfantVisit

#from .base_model_form import BaseModelForm
from bhp077.apps.microbiome_infant.forms import BaseInfantModelForm


class InfantDeathForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(InfantDeathForm, self).clean()
        if cleaned_data.get('death_reason_hospitalized'):
            if ('specify' in cleaned_data.get('death_reason_hospitalized').name
                    and not cleaned_data.get('death_reason_hospitalized_other')):
                raise forms.ValidationError('Please specify further details for the reason hospitalized.')
        return cleaned_data

    class Meta:
        model = InfantDeath
        fields = '__all__'
