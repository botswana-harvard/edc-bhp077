from django.db.models import get_model

from edc.subject.off_study.mixins import OffStudyMixin


class MaternalOffStudyMixin(OffStudyMixin):

    def get_off_study_cls(self):
        from .maternal_off_study import MaternalOffStudy
        return MaternalOffStudy

    @property
    def OFF_STUDY_MODEL(self):
        return get_model('microbiome_maternal', 'MaternalOffStudy')

    class Meta:
        abstract = True
