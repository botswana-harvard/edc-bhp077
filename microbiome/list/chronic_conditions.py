from edc_base.model.models import BaseListModel


class ChronicConditions (BaseListModel):

    class Meta:
        app_label = "microbiome"
        verbose_name = "ChronicConditions"
        verbose_name_plural = "ChronicConditions"
