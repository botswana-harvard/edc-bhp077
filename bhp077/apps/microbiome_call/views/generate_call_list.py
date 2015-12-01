from __future__ import print_function
from django.views.generic import TemplateView

from ..models import AntenatalCallList
from ...microbiome_maternal.models import AntenatalEnrollment, MaternalConsent


class GenerateCallList(TemplateView):
    template_name = "generate_call_list.html"

    def get_context_data(self, **kwargs):
        context = super(GenerateCallList, self).get_context_data(**kwargs)
        context.update(
            search_result=self.create_antenatal_call_list(),
        )
        return context

    def create_antenatal_call_list(self):
        """Create antenatal call list."""
        antenatal_enrollments = AntenatalEnrollment.objects.filter(antenatal_eligible=True)
        if antenatal_enrollments:
            for antenatal_enrollment in antenatal_enrollments:
                    try:
                        AntenatalCallList.objects.get(antenatal_enrollment=antenatal_enrollment)
                    except AntenatalCallList.DoesNotExist:
                        try:
                            maternal_consent = MaternalConsent.objects.get(registered_subject=antenatal_enrollment.registered_subject)
                        except MaternalConsent.DoesNotExist:
                            pass
                        AntenatalCallList.objects.create(
                            antenatal_enrollment=antenatal_enrollment,
                            consent_datetime=maternal_consent.consent_datetime,
                            first_name=maternal_consent.first_name,
                            initials=maternal_consent.initials
                        )
            return AntenatalCallList.objects.filter(antenatal_enrollment__in=antenatal_enrollments)
        return None
