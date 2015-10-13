from edc_base.audit_trail import AuditTrail
from edc.subject.off_study.models import BaseOffStudy
from edc_base.model.models.base_uuid_model import BaseUuidModel


class MaternalOffStudy(BaseOffStudy, BaseUuidModel):

    """A model completed by the user that completed when the subject is taken off-study."""

    history = AuditTrail()

    class Meta:
        app_label = "microbiome"
        verbose_name = "Maternal Off Study"
        verbose_name_plural = "Maternal Off Study"
