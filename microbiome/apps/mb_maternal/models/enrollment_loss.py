from django.db import models
from django.utils import timezone

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_sync.models import SyncModelMixin

from ..managers import AntenatalEnrollmentLossManager, PostnatalEnrollmentLossManager

from .antenatal_enrollment import AntenatalEnrollment
from .postnatal_enrollment import PostnatalEnrollment


class BaseEnrollmentLoss(SyncModelMixin, BaseUuidModel):
    """ A model triggered and completed by system when a mother fails enrollment. """

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        default=timezone.now,
        help_text='Date and time of report.')

    reason_unenrolled = models.TextField(
        verbose_name='Reason not enrolled',
        max_length=500,
        help_text='Gets reasons from Antental and/or Postnatal Enrollment')

    history = AuditTrail()

    def unenrollment(self):
        return self.reason_unenrolled or []
    reason_unenrolled.allow_tags = True

    class Meta:
        abstract = True


class AntenatalEnrollmentLoss(BaseEnrollmentLoss):
    """ A model triggered and completed by system when a mother fails antenatal enrollment"""

    antenatal_enrollment = models.OneToOneField(AntenatalEnrollment)

    objects = AntenatalEnrollmentLossManager()

    def natural_key(self):
        return self.antenatal_enrollment.natural_key()
    natural_key.dependencies = ['mb_maternal.antenatalenrollment', ]

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = 'ANT Enrollment Loss'
        verbose_name_plural = 'ANT Enrollment Loss'


class PostnatalEnrollmentLoss(BaseEnrollmentLoss):
    """ A model triggered and completed by system when a mother fails postnatal enrollment"""

    postnatal_enrollment = models.OneToOneField(PostnatalEnrollment)

    objects = PostnatalEnrollmentLossManager()

    def natural_key(self):
        return self.postnatal_enrollment.natural_key()
    natural_key.dependencies = ['mb_maternal.postnatalenrollment', ]

    class Meta:
        app_label = 'mb_maternal'
        verbose_name = 'PNT Enrollment Loss'
        verbose_name_plural = 'PNT Enrollment Loss'
