from edc_base.model.models import BaseListModel


class DiseasesAtEnrollment (BaseListModel):

    class Meta:
        app_label = "microbiome_list"
        verbose_name = "Diseases At Enrollment"
        verbose_name_plural = "Diseases At Enrollment"
