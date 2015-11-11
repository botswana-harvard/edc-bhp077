from edc.subject.off_study.mixins import OffStudyMixin


class MaternalOffStudyMixin(OffStudyMixin):

    def get_off_study_cls(self):
        from .maternal_off_study import MaternalOffStudy
        return MaternalOffStudy

    def save(self, *args, **kwargs):
        self.OFF_STUDY_MODEL = self.get_off_study_cls()
        super(MaternalOffStudyMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
