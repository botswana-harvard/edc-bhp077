import factory
from django.utils import timezone

from edc_constants.constants import YES, NO, POS, NEG
from bhp077.apps.microbiome.constants import LIVE

from edc.subject.registration.tests.factories import RegisteredSubjectFactory

from bhp077.apps.microbiome_maternal.models import PostnatalEnrollment


class PostnatalEnrollmentFactory(factory.DjangoModelFactory):

    class Meta:
        model = PostnatalEnrollment

    report_datetime = timezone.now()
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    on_tb_treatment = NO
    breastfeed_for_a_year = YES
    instudy_for_a_year = YES
    verbal_hiv_status = NEG
    delivery_type = YES
    gestation_before_birth = 37
    live_or_still_birth = LIVE
    live_infants = 1
    is_diabetic = NO
    #evidence_hiv_status = YES
    #valid_regimen = YES
    #date_of_rapid_test = timezone.now().date()
    postpartum_days = 2


