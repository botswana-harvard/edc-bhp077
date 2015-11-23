from django.db import models
from datetime import datetime

from edc.subject.appointment_helper.models import BaseAppointmentMixin
from edc.subject.registration.models import RegisteredSubject
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc_consent.models import RequiresConsentMixin
from edc_consent.models.fields import SampleCollectionFieldsMixin, VulnerabilityFieldsMixin
from edc_consent.models.validators import eligible_if_yes_or_declined
from edc_constants.choices import YES_NO_DECLINED
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE

from .maternal_consent import MaternalConsent


class SampleConsent(SampleCollectionFieldsMixin, RequiresConsentMixin, VulnerabilityFieldsMixin,
                    BaseUuidModel, BaseAppointmentMixin):

    CONSENT_MODEL = MaternalConsent

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    report_datetime = models.DateTimeField(
        verbose_name="Date and Time of Sample Consent",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=datetime.now,
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                   'the date/time this information was reported.'))

    consent_benefits = models.CharField(
        verbose_name=("I have explained the purpose of the sample storage"
                      " to the participant. To the best of my knowledge, she understands"
                      " the purpose, procedures, risks and benefits to her and her baby."),
        max_length=15,
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default=NOT_APPLICABLE,
        help_text="answer is N/A if participant declines sample storage")

    consent_copy = models.CharField(
        verbose_name=("I have provided the client with a copy of their signed informed consent"),
        max_length=20,
        choices=YES_NO_DECLINED,
        validators=[eligible_if_yes_or_declined, ],
        null=True,
        blank=False,
        help_text="If declined, return copy to the clinic with the consent",
    )

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    def __unicode__(self):
        return "{0}".format(self.registered_subject.subject_identifier)

    def get_report_datetime(self):
        return self.report_datetime

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Sample Consent'
        verbose_name_plural = 'Sample Consent'
