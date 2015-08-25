from django.db import models
from django.core.urlresolvers import reverse

from edc.audit.audit_trail import AuditTrail
from edc.choices.common import YES_NO
from edc.base.model.fields.custom.custom_fields import OtherCharField, IsDateEstimatedField

from apps.mpepu_list.models.maternal_enroll import PriorArv
from apps.mpepu.choices import PRIOR_PREG_HAART_STATUS

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .maternal_enroll import MaternalEnroll


class MaternalEnrollArv(BaseScheduledVisitModel):

    """Model for Maternal Enrollment: ARV History"""

    maternal_enroll = models.OneToOneField(MaternalEnroll)

    haart_start_date = models.DateField(
        verbose_name="Date of HAART first started",
        help_text="",
        )
    is_date_estimated = IsDateEstimatedField(
        verbose_name=("Is the subject's date of HAART estimated?"),
        )
    preg_on_haart = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Was she still on HAART at the time she became pregnant for this pregnancy? ",
        help_text="",
        )
    haart_changes = models.IntegerField(
        verbose_name="How many times did you change your HAART medicines?",
        help_text="",
        )
    prior_preg = models.CharField(
        max_length=80,
        verbose_name="Prior to this pregnancy the mother has ",
        choices=PRIOR_PREG_HAART_STATUS,
        help_text="",
        )
    prior_arv = models.ManyToManyField(PriorArv,
        verbose_name="Please list all of the ARVs that the mother ever received prior to the current pregnancy:",
        help_text="",
        )
    prior_arv_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,
        )

    history = AuditTrail()

    def __unicode__(self):
        return "%s" % (self.maternal_enroll)

    def get_absolute_url(self):
        return reverse('admin:mpepu_maternal_maternalenrollarv_change', args=(self.id,))

    class Meta:
        app_label = 'microbiome'
