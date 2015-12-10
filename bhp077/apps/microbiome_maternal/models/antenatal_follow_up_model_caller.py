from edc_call_manager.model_caller import ModelCaller, WEEKLY
from edc_call_manager.decorators import register

from .antenatal_enrollment import AntenatalEnrollment
from .maternal_consent import MaternalConsent
from .postnatal_enrollment import PostnatalEnrollment
from .maternal_locator import MaternalLocator


@register(AntenatalEnrollment)
class AnteNatalFollowUpModelCaller(ModelCaller):
    label = 'Antenatal-to-Postnatal'
    consent_model = MaternalConsent
    locator_model = MaternalLocator
    unscheduling_model = PostnatalEnrollment
    interval = WEEKLY
