from django.forms import ModelForm

from ..models import MaternalEligibilityPre


class MaternalEligibilityPreForm(ModelForm):

    class Meta:
        model = MaternalEligibilityPre
        fields = '__all__'
