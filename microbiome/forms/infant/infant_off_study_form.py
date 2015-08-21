from django.forms.models import ModelForm

from microbiome.models.microbiome_infant import InfantOffStudy


class InfantOffStudyForm(ModelForm):

    class Meta:
        model = InfantOffStudy
        fields = '__all__'
