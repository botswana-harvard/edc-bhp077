from django.forms import ModelForm

from ..models import MaternalEligibilityPost


class MaternalEligibilityPostForm(ModelForm):

    class Meta:
        model = MaternalEligibilityPost
        fields = '__all__'
