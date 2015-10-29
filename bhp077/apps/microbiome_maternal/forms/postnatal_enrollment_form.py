from edc.base.form.forms import BaseModelForm
from ..models import PostnatalEnrollment


class PostnatalEnrollmentForm(BaseModelForm):

    class Meta:
        model = PostnatalEnrollment
        fields = '__all__'
