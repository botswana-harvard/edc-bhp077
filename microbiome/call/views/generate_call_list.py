# some_app/views.py
from django.views.generic import TemplateView

from ..models import AntenatalCallList, PostnatalCallList
from ...maternal.models import AntenatalEnrollment


class GenerateCallList(TemplateView):
    template_name = "generate_call_list.html"

    def get_context_data(self, **kwargs):
        context = super(GenerateCallList, self).get_context_data(**kwargs)
        return context

    def create_antenatal_call_list(self):
        """Create antenatal call list."""
        antenatal_enrollments = AntenatalEnrollment.objects.filter(weeks_of_gestation=32)
        if antenatal_enrollments:
            for antenatal_enrollment in antenatal_enrollments:
                try:
                    AntenatalCallList.objects.get(antenatal_enrollment=antenatal_enrollment)
                except AntenatalCallList.DoesNotExist:
                    AntenatalCallList.objects.create(antenatal_enrollment=antenatal_enrollment)

    def create_postnatal_call_list(self):
        """Create postnatal call list."""
        try:
            pass
        except:
            pass
