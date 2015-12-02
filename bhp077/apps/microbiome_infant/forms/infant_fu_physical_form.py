from django import forms

from ..models import InfantFuPhysical

from .base_infant_model_form import BaseInfantModelForm
from edc.subject.registration.models import registered_subject


class InfantFuPhysicalForm(BaseInfantModelForm):

    def clean(self):
        cleaned_data = super(InfantFuPhysicalForm, self).clean()
        self.validate_height(cleaned_data)
        self.validate_head_circum(cleaned_data)
        return cleaned_data

    def validate_height(self, cleaned_data):
        visit = ['2000', '2010', '2030', '2060', '2090', '2120']

        if (
            not cleaned_data.get('infant_visit').appointment.visit_definition.code == '2000' and
            not cleaned_data.get('infant_visit').appointment.visit_definition.code == '2010'
        ):
            prev_visit = visit.index(cleaned_data.get('infant_visit').appointment.visit_definition.code) - 1
            while prev_visit > 0:
                try:
                    prev_fu_phy = InfantFuPhysical.objects.get(infant_visit__appointment__registered_subject=
                                                          cleaned_data.get('infant_visit').appointment.registered_subject,
                                                          infant_visit__appointment__visit_definition__code=
                                                          visit[prev_visit])
                    if cleaned_data.get('height') < prev_fu_phy.height:
                        raise forms.ValidationError('You stated that the height for the participant as {}, yet in visit {} '
                                                    'you indicated that participant height was {}. Please correct.'
                                                    .format(cleaned_data.get('height'), visit[prev_visit], prev_fu_phy.height))
                    break
                except InfantFuPhysical.DoesNotExist:
                    prev_visit = prev_visit - 1

    def validate_head_circum(self, cleaned_data):
        visit = ['2000', '2010', '2030', '2060', '2090', '2120']

        if (
            not cleaned_data.get('infant_visit').appointment.visit_definition.code == '2000' and
            not cleaned_data.get('infant_visit').appointment.visit_definition.code == '2000'
        ):
            prev_visit = visit.index(cleaned_data.get('infant_visit').appointment.visit_definition.code) - 1
            while prev_visit > 0:
                try:
                    prev_fu_phy = InfantFuPhysical.objects.get(infant_visit__appointment__registered_subject=
                                                          cleaned_data.get('infant_visit').appointment.registered_subject,
                                                          infant_visit__appointment__visit_definition__code=
                                                          visit[prev_visit])
                    if cleaned_data.get('head_circumference') < prev_fu_phy.head_circumference:
                        raise forms.ValidationError('You stated that the head circumference for the participant as {}, '
                                                    'yet in visit {} you indicated that participant height was {}. '
                                                    'Please correct.'.format(cleaned_data.get('head_circumference'),
                                                                             visit[prev_visit], prev_fu_phy.head_circumference))
                    break
                except InfantFuPhysical.DoesNotExist:
                    prev_visit = prev_visit - 1

    class Meta:
        model = InfantFuPhysical
        fields = '__all__'
