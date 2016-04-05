from edc_base.model.models import BaseListModel


class Supplements (BaseListModel):

    class Meta:
        app_label = 'mb_list'
        verbose_name = "Supplements"
        verbose_name_plural = "Supplements"
