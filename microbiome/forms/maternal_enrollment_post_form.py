from django import forms

from ..models import MaternalEnrollmentPost

class MaternalEnrollmentPostForm(forms.ModelForm):

    class Meta:
        model = MaternalEnrollmentPost
        fields = '__all__'
