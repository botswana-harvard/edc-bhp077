from edc_base.model.models import BaseListModel


class Contraceptives (BaseListModel):

    class Meta:
        app_label = "microbiome_list"
        verbose_name = "Contraceptives"
        verbose_name_plural = "Contraceptives"
