from edc.subject.off_study.mixins import OffStudyMixin


class MaternalOffStudyMixin(OffStudyMixin):

    def get_off_study_cls(self):
        from .maternal_off_study import MaternalOffStudy
        return MaternalOffStudy

    @property
    def OFF_STUDY_MODEL(self):
        from .maternal_off_study import MaternalOffStudy
        return MaternalOffStudy

    def save(self, *args, **kwargs):
        super(MaternalOffStudyMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
