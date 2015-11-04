from django.db.models import get_model

from edc.subject.off_study.mixins import OffStudyMixin


class MaternalOffStudyMixin(OffStudyMixin):

    def get_off_study_cls(self):
        from .maternal_off_study import MaternalOffStudy
        return MaternalOffStudy

    def save(self, *args, **kwargs):
        self.OFF_STUDY_MODEL = get_model("microbiome_maternal", "MaternalOffStudy")
        super(MaternalOffStudyMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
