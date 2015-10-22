from django.db import models
from django.core.urlresolvers import reverse

from edc.audit.audit_trail import AuditTrail
from edc.choices.common import YES_NO, YES_NO_NA

from ..infant_choices import STOOL_COLLECTION_TIME, STOOL_STORED

from .infant_scheduled_visit_model import InfantScheduledVisitModel


class InfantStoolCollection(InfantScheduledVisitModel):

    """Infant stool collection. Used in every visit from birth to 12 months"""

    sample_obtained = models.CharField(
        verbose_name="A stool sample/specimen can be obtained from the nappy of this child today ",
        choices=YES_NO,
        max_length=3,
        help_text=("If a stool samples/specimen cannot be obtained today, do not complete the"
                   " remainder of this form"),
    )

    stool_colection = models.CharField(
        verbose_name="Was the stool sample from the nappy collected in real-time "
                     "(stool produced at study visit) or brought by the mother?",
        choices=STOOL_COLLECTION_TIME,
        max_length=20,
        help_text=(""),
    )

    stool_colection_time = models.IntegerField(
        verbose_name="Approximately how many hours ago did the mother/caregiver collect the stool in the nappy?",
        help_text=("Cannot exceed 24 hours"),
    )

    stool_stored = models.CharField(
        verbose_name="Was the sample stored?",
        choices=STOOL_STORED,
        max_length=40,
        help_text=("")
    )

    past_diarrhea = models.CharField(
        verbose_name="Has this infant/child had diarrhea in the past 7 days?",
        choices=YES_NO,
        max_length=3,
        null=True,
        blank=True,
        help_text=("Diarrhea is defined as 3 or more loose or watery stools with or without blood"
                   " over a 24 hour period and the stool pattern is a change from the"
                   " infant's/child's normal stool pattern"),
    )

    diarrhea_past_24hrs = models.CharField(
        verbose_name=("If the child has had diarrhea in the last 7 days, has the child's"
                      " diarrhea continued in the last 24 hours?"),
        max_length=15,
        choices=YES_NO_NA,
        null=True,
        blank=True,
        help_text="",
    )

    antibiotics_7days = models.CharField(
        verbose_name="Has this infant/child taken antibiotics in the past 7 days, other than CTX/Placebo?",
        choices=YES_NO,
        max_length=3,
        null=True,
        blank=True,
        help_text=("If the answer to this question is yes, please ensure that antibiotic"
                   " information is recorded on NEW MEDICATIONS EDC form"),
    )

    antibiotic_dose_24hrs = models.CharField(
        verbose_name=("If this infant/child has taken antibiotics in the past 7 days, have they"
                      " taken a dose in the last 24 hours, other than CTX/Placebo?"),
        max_length=15,
        choices=YES_NO_NA,
        null=True,
        blank=True,
        help_text="",
    )

    history = AuditTrail()

    objects = models.Manager()

    def __unicode__(self):
        return "%s" % (self.infant_visit)

    def get_absolute_url(self):
        return reverse('admin:mpepu_infant_infantstoolcollection_change', args=(self.id,))

    class Meta:
        app_label = "mpepu_infant"
        verbose_name = "Infant Stool Collection"
        verbose_name_plural = "Infant Stool Collection"
