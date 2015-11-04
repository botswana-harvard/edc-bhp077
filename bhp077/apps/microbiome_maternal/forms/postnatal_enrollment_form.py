from edc.base.form.forms import BaseModelForm
from ..models import PostnatalEnrollment, AntenatalEnrollment

from edc.subject.registration.models import RegisteredSubject


class PostnatalEnrollmentForm(BaseModelForm):

    class Meta:
        model = PostnatalEnrollment
        fields = '__all__'
