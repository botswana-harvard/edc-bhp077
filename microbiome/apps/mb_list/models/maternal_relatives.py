from edc_base.model.models import BaseListModel


class MaternalRelatives(BaseListModel):

    class Meta:
        app_label = 'mb_list'
        verbose_name = "Maternal Relatives"
        verbose_name_plural = "Maternal Relatives"
