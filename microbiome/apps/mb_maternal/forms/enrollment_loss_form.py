from django.forms import ModelForm

from ..models.enrollment_loss import AntenatalEnrollmentLoss, PostnatalEnrollmentLoss


class AntenatalEnrollmentLossForm(ModelForm):

    class Meta:
        model = AntenatalEnrollmentLoss
        fields = '__all__'


class PostnatalEnrollmentLossForm(ModelForm):

    class Meta:
        model = PostnatalEnrollmentLoss
        fields = '__all__'
