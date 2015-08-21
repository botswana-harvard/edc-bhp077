from django.forms.models import ModelForm

from microbiome.models.microbiome_infant import InfantVisit


class InfantVisit(ModelForm):

    class Meta:
        model = InfantVisit
        fields = '__all__'
