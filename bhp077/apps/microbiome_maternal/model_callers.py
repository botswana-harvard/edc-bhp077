from edc_call_manager.model_caller import ModelCaller, WEEKLY
from edc_call_manager.decorators import register

from .models import (
    MaternalConsent, MaternalLocator, AntenatalEnrollment, PostnatalEnrollment)


@register(AntenatalEnrollment)
class AnteNatalModelCaller(ModelCaller):
    label = 'Antenatal-followup'
    consent_model = MaternalConsent
    locator_model = MaternalLocator
    locator_filter = 'maternal_visit__appointment__registered_subject__subject_identifier'
    unscheduling_model = PostnatalEnrollment
    interval = WEEKLY
