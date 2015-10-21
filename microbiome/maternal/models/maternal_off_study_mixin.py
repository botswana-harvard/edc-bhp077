from .maternal_off_study import MaternalOffStudy

from edc.subject.off_study.mixins import OffStudyMixin


class MaternalOffStudyMixin(OffStudyMixin):

    OFF_STUDY_MODEL = MaternalOffStudy

    class Meta:
        abstract = True
