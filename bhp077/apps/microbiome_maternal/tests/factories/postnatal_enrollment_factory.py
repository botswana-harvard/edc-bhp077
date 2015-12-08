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
    vaginal_delivery = YES
    on_tb_tx = NO
    delivery_status = LIVE
    gestation_wks_delivered = 38
    will_breastfeed = YES
    will_remain_onstudy = YES
    current_hiv_status = POS
    evidence_hiv_status = YES
    valid_regimen = YES
    valid_regimen_duration = YES
    rapid_test_done = NO
    rapid_test_date = timezone.now().date()
    delivery_status = LIVE
    live_infants = 1
    postpartum_days = 2
