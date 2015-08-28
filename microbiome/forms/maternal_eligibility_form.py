from django.forms import ModelForm

from ..models import MaternalEligibility


class MaternalEligibilityForm(ModelForm):

    class Meta:
        model = MaternalEligibility
        fields = '__all__'
