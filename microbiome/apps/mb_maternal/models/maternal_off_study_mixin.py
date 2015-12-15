from edc_offstudy.models import OffStudyMixin


class MaternalOffStudyMixin(OffStudyMixin):

    OFF_STUDY_MODEL = ('microbiome_maternal', 'MaternalOffStudy')

    class Meta:
        abstract = True
