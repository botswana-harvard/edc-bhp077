from edc.subject.off_study.mixins import OffStudyMixin

from .maternal_off_study import MaternalOffStudy


class MaternalOffStudyMixin(OffStudyMixin):

    OFF_STUDY_MODEL = MaternalOffStudy

    class Meta:
        abstract = True
