from django import forms

from edc.subject.off_study.forms import BaseOffStudyForm
from ..models import MaternalOffStudy


class MaternalOffStudyForm (BaseOffStudyForm):

    class Meta:
        model = MaternalOffStudy
