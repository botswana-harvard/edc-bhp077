from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE

from ..choices import STOOL_COLLECTION_TIME, STOOL_STORED, NAPPY_TYPE

from .infant_crf_visit_model import InfantCrfModel


class InfantStoolCollection(InfantCrfModel):

    """ Infant stool collection. Used in every visit from birth to 12 months. """

    sample_obtained = models.CharField(
        verbose_name="A stool sample/specimen can be obtained from the nappy of this child today ",
        choices=YES_NO,
        max_length=3,
        help_text=("If a stool samples/specimen cannot be obtained today, do not complete the"
                   " remainder of this form"),
    )

    nappy_type = models.CharField(
        verbose_name="What type of nappy was used?",
        choices=NAPPY_TYPE,
        default=NOT_APPLICABLE,
        max_length=20,
    )

    other_nappy = OtherCharField(
        verbose_name='If other, specify...',
        max_length=25,
        blank=True,
        null=True,
    )

    stool_collection = models.CharField(
        verbose_name="Was the stool sample from the nappy collected in real-time "
                     "(stool produced at study visit) or brought by the mother?",
        choices=STOOL_COLLECTION_TIME,
        default=NOT_APPLICABLE,
        max_length=20,
    )

    stool_collection_time = models.IntegerField(
        verbose_name="Approximately how many hours ago did the mother/caregiver collect the stool in the nappy?",
        help_text=("Cannot exceed 24 hours"),
        validators=[MinValueValidator(0), MaxValueValidator(24)],
        blank=True,
        null=True,
    )

    stool_stored = models.CharField(
        verbose_name="How was the sample stored?",
        choices=STOOL_STORED,
        default=NOT_APPLICABLE,
        max_length=40,
    )

    past_diarrhea = models.CharField(
        verbose_name="Has this infant/child had diarrhea in the past 7 days?",
        choices=YES_NO_NA,
        max_length=15,
        default=NOT_APPLICABLE,
        help_text=("Diarrhea is defined as 3 or more loose or watery stools with or without blood"
                   " over a 24 hour period and the stool pattern is a change from the"
                   " infant's/child's normal stool pattern"),
    )

    diarrhea_past_24hrs = models.CharField(
        verbose_name=("If the child has had diarrhea in the last 7 days, has the child's"
                      " diarrhea continued in the last 24 hours?"),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    antibiotics_7days = models.CharField(
        verbose_name="Has this infant/child taken antibiotics in the past 7 days?",
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        max_length=15,
        help_text=("If the answer to this question is yes, please ensure that antibiotic"
                   " information is recorded on NEW MEDICATIONS EDC form"),
    )

    antibiotic_dose_24hrs = models.CharField(
        verbose_name=("If this infant/child has taken antibiotics in the past 7 days, have they"
                      " taken a dose in the last 24 hours?"),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    history = AuditTrail()

    class Meta:
        app_label = 'mb_infant'
        verbose_name = "Infant Stool Collection"
        verbose_name_plural = "Infant Stool Collection"
