from django.db import models
from datetime import datetime

from bhp077.apps.microbiome.choices import DRUG_RELATIONSHIP

from edc_base.audit_trail import AuditTrail

from edc.subject.adverse_event.models import BaseDeathReport
from edc_consent.models import RequiresConsentMixin
from edc.data_manager.models import TimePointStatusMixin
from edc.entry_meta_data.managers import EntryMetaDataManager
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future

from .infant_scheduled_visit_model import InfantScheduledVisitModel
from .infant_off_study_mixin import InfantOffStudyMixin
from .infant_visit import InfantVisit


class InfantDeath (InfantScheduledVisitModel, BaseDeathReport):

    death_reason_hospitalized_other = models.TextField(
        verbose_name="if other illness or pathogen specify or non infectious reason, please specify below:",
        max_length=250,
        blank=True,
        null=True,
    )

    study_drug_relate = models.CharField(
        verbose_name="Relationship between the participant death and study drug (CTX vs Placebo)",
        max_length=25,
        choices=DRUG_RELATIONSHIP,
    )

    infant_nvp_relate = models.CharField(
        verbose_name="Relationship between the participant death and infant extended nevirapine prophylaxis ",
        max_length=25,
        choices=DRUG_RELATIONSHIP,
    )

    haart_relate = models.CharField(
        verbose_name="Relationship between the participant death and HAART",
        max_length=25,
        choices=DRUG_RELATIONSHIP,
    )

    trad_med_relate = models.CharField(
        verbose_name="Relationship between the participant death and traditional medicine use",
        max_length=25,
        choices=DRUG_RELATIONSHIP,
    )

    objects = models.Manager()

    history = AuditTrail()

    entry_meta_data_manager = EntryMetaDataManager(InfantVisit)

    class Meta:
        app_label = "microbiome_infant"
        verbose_name = "Infant Death"
