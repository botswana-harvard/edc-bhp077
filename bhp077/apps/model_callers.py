from edc_call_manager.model_caller import ModelCaller, WEEKLY
from edc_call_manager.decorators import register

from .microbiome_maternal.models import (
    MaternalConsent, MaternalLocator, AntenatalEnrollment, PostnatalEnrollment)


@register(AntenatalEnrollment)
class AnteNatalModelCaller(ModelCaller):
    label = 'Antenatal-to-Postnatal'
    consent_model = MaternalConsent
    locator_model = MaternalLocator
    unscheduling_model = PostnatalEnrollment
    interval = WEEKLY
