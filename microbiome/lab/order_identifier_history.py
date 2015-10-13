from edc.core.identifier.models import BaseIdentifierModel
from edc_base.model.models import BaseUuidModel


class OrderIdentifierHistory(BaseIdentifierModel, BaseUuidModel):

    class Meta:
        app_label = "lab"
