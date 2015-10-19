from django.forms import ModelForm

from ..models import PostnatalEnrollment


class PostnatalEnrollmentForm(ModelForm):

    class Meta:
        model = PostnatalEnrollment
        fields = '__all__'
