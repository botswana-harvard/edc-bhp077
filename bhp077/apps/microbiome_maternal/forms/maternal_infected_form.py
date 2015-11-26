from ..models import MaternalInfected

from base_maternal_model_form import BaseMaternalModelForm


class MaternalInfectedForm(BaseMaternalModelForm):

    def clean(self):
        cleaned_data = super(MaternalInfectedForm, self).clean()
        return cleaned_data

    class Meta:
        model = MaternalInfected
        fields = '__all__'
