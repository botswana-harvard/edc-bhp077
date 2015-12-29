from edc.core.identifier.models import BaseIdentifierModel
from edc_base.model.models import BaseUuidModel
from edc_sync.models import SyncModelMixin


class OrderIdentifierHistory(BaseIdentifierModel, SyncModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'mb_lab'
