from edc.base.form.forms import BaseModelForm

from ..models import AntenatalEnrollment


class AntenatalEnrollmentForm(BaseModelForm):

    class Meta:
        model = AntenatalEnrollment
        fields = '__all__'
