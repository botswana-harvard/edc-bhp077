import factory

from django.utils import timezone

from edc_constants.choices import YES, NO

from edc.subject.registration.tests.factories import RegisteredSubjectFactory

from microbiome.apps.mb_maternal.models import AntenatalEnrollment


class AntenatalEnrollmentFactory(factory.DjangoModelFactory):

    class Meta:
        model = AntenatalEnrollment

    report_datetime = timezone.now()

    gestation_wks = 36
    on_hypertension_tx = NO
    is_diabetic = NO
    on_tb_tx = NO
    valid_regimen = YES
    valid_regimen_duration = YES
    week32_test = YES
    will_breastfeed = YES
    will_remain_onstudy = YES
