from django.forms import ModelForm

from ..models import AntenatalEnrollment


class AntenatalEnrollmentForm(ModelForm):

    class Meta:
        model = AntenatalEnrollment
        fields = '__all__'
