from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer

from ..models import InfantVisit
from .base_infant_model_form import BaseInfantModelForm
from bhp077.apps.microbiome.choices import VISIT_REASON, VISIT_INFO_SOURCE


class InfantVisitForm(BaseInfantModelForm):

    reason = forms.ChoiceField(
        label='Reason for visit',
        choices=[choice for choice in VISIT_REASON],
        help_text="",
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    info_source = forms.ChoiceField(
        label='Source of information',
        choices=[choice for choice in VISIT_INFO_SOURCE],
        widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer))

    class Meta:
        model = InfantVisit
        fields = '__all__'
