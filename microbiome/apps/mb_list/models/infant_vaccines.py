from edc_base.model.models import BaseListModel


class InfantVaccines (BaseListModel):

    class Meta:
        app_label = 'mb_list'
        verbose_name = "Infant Vaccines"
        verbose_name_plural = "Infant Vaccines"
