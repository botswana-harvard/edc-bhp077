from django.core.validators import RegexValidator
from django.db import models

from edc.device.sync.models import BaseSyncUuidModel
from edc_base.audit_trail import AuditTrail
from edc_base.encrypted_fields import EncryptedTextField
from edc_base.model.fields import OtherCharField
from edc_base.model.validators import date_is_future
from edc_constants.choices import YES_NO_UNKNOWN, TIME_OF_DAY, TIME_OF_WEEK, YES_NO
from edc_constants.constants import YES


# from ..managers import AntenatalCallLogManager

from ..choices import CONTACT_TYPE, APPT_GRADING, APPT_LOCATIONS


from .antenatal_call_list import AntenatalCallList
# from ..managers.antenatal_call_log_manager import AntenatalCallLogEntryManager


class AntenatalCallLog(BaseSyncUuidModel):

    """A system model completed by the user on the after contacting an antenatal participant"""
    antenatal_call_list = models.ForeignKey(AntenatalCallList)

    locator_information = EncryptedTextField(
        help_text='This information has been imported from the previous locator. You may update as required.')

    contact_notes = EncryptedTextField(
        null=True,
        blank=True,
        help_text='')

    history = AuditTrail()

#     objects = AntenatalCallLogManager()

    def __unicode__(self):
        return '{} {}'.format(
            self.antenatal_call_list.first_name,
            self.antenatal_call_list.initials)

    def save(self, *args, **kwargs):
        super(AntenatalCallLog, self).save(*args, **kwargs)

    def natural_key(self):
        return self.antenatal_call_list.natural_key()

    class Meta:
        app_label = 'microbiome_call'


class AntenatalCallLogEntry(BaseSyncUuidModel):

    antenatal_call_log = models.ForeignKey(AntenatalCallLog)

    call_datetime = models.DateTimeField()

    invalid_numbers = models.CharField(
        verbose_name='Indicate any invalid numbers dialed from the locator information above?',
        max_length=50,
        validators=[RegexValidator(
            regex=r'^[0-9]{7,8}(,[0-9]{7,8})*$',
            message='Only enter contact numbers separated by commas. No spaces and no trailing comma.'), ],
        null=True,
        blank=True,
        help_text='Separate by comma (,).'
    )

    contact_type = models.CharField(
        max_length=15,
        choices=CONTACT_TYPE,
        help_text='If no contact made. STOP. Save form.'
    )

    time_of_week = models.CharField(
        verbose_name='Time of week when participant will be available',
        max_length=25,
        choices=TIME_OF_WEEK,
        blank=True,
        null=True,
        help_text=""
    )

    time_of_day = models.CharField(
        verbose_name='Time of day when participant will be available',
        max_length=25,
        choices=TIME_OF_DAY,
        blank=True,
        null=True,
        help_text=""
    )

    appt = models.CharField(
        verbose_name='Is the participant willing to schedule an appointment',
        max_length=7,
        choices=YES_NO_UNKNOWN,
        null=True,
        blank=True,
        help_text=""
    )

    appt_date = models.DateField(
        verbose_name="Appointment Date",
        validators=[date_is_future],
        null=True,
        blank=True,
        help_text="This can only come from the participant."
    )

    appt_grading = models.CharField(
        verbose_name='Is this appointment...',
        max_length=25,
        choices=APPT_GRADING,
        null=True,
        blank=True,
        help_text=""
    )

    appt_location = models.CharField(
        verbose_name='Appointment location',
        max_length=50,
        choices=APPT_LOCATIONS,
        null=True,
        blank=True,
        help_text=""
    )

    appt_location_other = OtherCharField(
        verbose_name='Appointment location',
        max_length=50,
        null=True,
        blank=True,
        help_text=""
    )

    delivered = models.NullBooleanField(
        default=False,
        editable=False)

    call_again = models.CharField(
        verbose_name='Call the participant again?',
        max_length=10,
        choices=YES_NO,
        default=YES,
        help_text=''
    )

    history = AuditTrail()

#     objects = AntenatalCallLogEntryManager()

    def save(self, *args, **kwargs):
        super(AntenatalCallLogEntry, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{} {} {}'.format(
            self.antenatal_call_log.antenatal_call_list.first_name,
            self.antenatal_call_log.antenatal_call_list.initials,
        )

    def natural_key(self):
        return self.antenatal_call_log.natural_key() + (self.call_datetime, )

    class Meta:
        app_label = 'microbiome_call'
        unique_together = ['antenatal_call_log', 'call_datetime']
