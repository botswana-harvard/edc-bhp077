from django.db import models

from edc.device.sync.models import BaseSyncUuidModel
from edc_base.audit_trail import AuditTrail
from edc_base.encrypted_fields import FirstnameField
from edc_base.model.validators import datetime_not_future, datetime_not_before_study_start
from edc_constants.constants import CLOSED, OPEN, NEW

from ..managers import AntenatalCallListManager
from ...maternal.models import AntenatalEnrollment


class AntenatalCallList (BaseSyncUuidModel):

    antenatal_enrollment = models.ForeignKey(AntenatalEnrollment)

    call_datetime = models.DateTimeField(
        null=True,
        editable=False,
        help_text='last call datetime updated by call log entry',
    )

    app_label = models.CharField(
        max_length=25,
        editable=False)

    first_name = FirstnameField(
        verbose_name='First name',
        editable=False,
    )

    initials = models.CharField(
        verbose_name='Initials',
        max_length=3,
        editable=False,
    )

    consent_datetime = models.DateTimeField(
        verbose_name="Consent date and time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text="From Subject Consent."
    )

    call_attempts = models.IntegerField(
        default=0)

    call_outcome = models.TextField(
        max_length=150,
        null=True,
    )

    call_status = models.CharField(
        max_length=15,
        choices=(
            (NEW, 'New'),
            (OPEN, 'Open'),
            (CLOSED, 'Closed'),
        ),
        default=NEW,
    )

    history = AuditTrail()

    objects = AntenatalCallListManager()

    def __unicode__(self):
        return '{} {} {}'.format(
            self.antenatal_enrollment,
            self.first_name,
            self.initials,
        )

    class Meta:
        app_label = 'call'
