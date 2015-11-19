from django.db import models
from django.core.urlresolvers import reverse

from edc.subject.adverse_event.choices import GRADING_SCALE
from edc.subject.code_lists.models import WcsDxAdult
from edc_base.audit_trail import AuditTrail
from edc_base.model.fields.custom_fields import OtherCharField
from edc_base.model.models import BaseUuidModel
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE

from bhp077.apps.microbiome_list.models import ChronicConditions
from bhp077.apps.microbiome.choices import BREAST_CHOICE

from ..managers import MaternalPostFuDxTManager
from ..maternal_choices import DX
from .maternal_scheduled_visit_model import MaternalScheduledVisitModel
from .maternal_consent import MaternalConsent


class MaternalBreastHealth(MaternalScheduledVisitModel):

    """ General post-partum follow-up. """

    CONSENT_MODEL = MaternalConsent

    breast_feeding = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Is the mother currently breastfeeding?",
        help_text="",
    )

    has_mastitis = models.CharField(
        max_length=3,
        choices=YES_NO_NA,
        verbose_name="Is there evidence of mastitis?",
        help_text="",
    )

    mastitis = models.CharField(
        max_length=3,
        choices=BREAST_CHOICE,
        verbose_name="Where is mastitis evident?",
        help_text="",
        default=NOT_APPLICABLE,
    )

    has_lesions = models.CharField(
        max_length=3,
        choices=YES_NO_NA,
        verbose_name="Are there any lesions such as ulcers, vesicles or sores on the breasts?",
        help_text="",
    )

    lesions = models.CharField(
        max_length=3,
        choices=BREAST_CHOICE,
        verbose_name="Where are the lesions evident?",
        help_text="",
        default=NOT_APPLICABLE,
    )

    stop_breastfeeding = models.CharField(
        max_length=3,
        choices=YES_NO_NA,
        verbose_name="Was the mother advised to discontonue breastfeeding?",
        help_text="",
    )

    why_not_advised = models.CharField(
        max_length=100,
        verbose_name="Please provide a reason why breastfeeding cessation not advised?",
        help_text="",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = "microbiome_maternal"
        verbose_name = "Maternal Breast Health"
        verbose_name_plural = "Maternal Breast Health"
