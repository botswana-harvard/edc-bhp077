from django.forms import ModelForm

from ..models import MaternalScreening


class MaternalScreeningForm(ModelForm):

    class Meta:
        model = MaternalScreening
        fields = '__all__'
