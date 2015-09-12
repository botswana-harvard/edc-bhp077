from edc_base.model.models import BaseListModel


class DiseasesAtEnrollment (BaseListModel):

    class Meta:
        app_label = "microbiome"
        verbose_name = "Diseases At Enrollment"
