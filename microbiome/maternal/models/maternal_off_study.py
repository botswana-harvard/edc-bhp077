from django.db import models

from edc.entry_meta_data.managers import EntryMetaDataManager
from edc.subject.off_study.models import BaseOffStudy
from edc_base.audit_trail import AuditTrail
from edc_base.model.models.base_uuid_model import BaseUuidModel

from maternal.models.maternal_visit import MaternalVisit


class MaternalOffStudy(BaseOffStudy, BaseUuidModel):

    """A model completed by the user that completed when the subject is taken off-study."""

    history = AuditTrail()

    maternal_visit = models.OneToOneField(MaternalVisit)

    entry_meta_data_manager = EntryMetaDataManager(MaternalVisit)

    class Meta:
        app_label = "microbiome"
        verbose_name = "Maternal Off Study"
        verbose_name_plural = "Maternal Off Study"
