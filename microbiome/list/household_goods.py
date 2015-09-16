from edc_base.model.models import BaseListModel


class HouseholdGoods (BaseListModel):

    class Meta:
        app_label = "microbiome"
        verbose_name = "Household Goods"
        verbose_name_plural = "Household Goods"
