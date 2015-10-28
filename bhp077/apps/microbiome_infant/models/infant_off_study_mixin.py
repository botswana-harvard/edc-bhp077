from edc.subject.off_study.mixins.off_study_mixin import OffStudyMixin


class InfantOffStudyMixin(OffStudyMixin):

    def get_off_study_cls(self):
        from .infant_off_study import InfantOffStudy
        return InfantOffStudy

    class Meta:
        abstract = True
