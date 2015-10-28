from edc.subject.off_study.mixins import OffStudyMixin


class MaternalOffStudyMixin(OffStudyMixin):

    def get_off_study_cls(self):
        from .maternal_off_study import MaternalOffStudy
        return MaternalOffStudy

    class Meta:
        abstract = True
