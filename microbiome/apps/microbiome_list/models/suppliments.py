from edc_base.model.models import BaseListModel


class Suppliments (BaseListModel):

    class Meta:
        app_label = "microbiome_list"
        verbose_name = "Suppliments"
        verbose_name_plural = "Suppliments"
