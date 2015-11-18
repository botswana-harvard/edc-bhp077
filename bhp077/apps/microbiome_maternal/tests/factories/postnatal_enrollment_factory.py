import factory
from django.utils import timezone

from edc_constants.constants import YES, NO, POS
from edc.subject.registration.tests.factories import RegisteredSubjectFactory

from bhp077.apps.microbiome_maternal.models import PostnatalEnrollment
from bhp077.apps.microbiome.constants import LIVE


class PostnatalEnrollmentFactory(factory.DjangoModelFactory):

    class Meta:
        model = PostnatalEnrollment

    report_datetime = timezone.now()
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    is_diabetic = NO
    postpartum_days = 2
    delivery_type = YES
    on_tb_treatment = NO
    live_or_still_birth = LIVE
    gestation_before_birth = 38
    breastfeed_for_a_year = YES
    instudy_for_a_year = YES
    verbal_hiv_status = POS
    evidence_hiv_status = YES
    valid_regimen = YES
    valid_regimen_duration = YES
    process_rapid_test = NO
    date_of_rapid_test = timezone.now().date()
    live_or_still_birth = LIVE
    live_infants = 1
    postpartum_days = 2
