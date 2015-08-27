import re

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import render

from microbiome.models import MaternalScreening, SubjectConsent


class Option(object):

    def __init__(self, link_text, href, data_toggle, data_target):
        self.link_text = link_text
        self.href = href
        self.data_toggle = data_toggle
        self.data_target = data_target
        self.name = self.link_text.lower().replace(' ', '_')


class SubjectDashboardView(TemplateView):
    template_name = 'dashboard.html'

    def __init__(self, **kwargs):
        super(SubjectDashboardView, self).__init__(**kwargs)
        self.context = None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SubjectDashboardView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title="Microbiome",
            left_sidebar_options=[
                Option('Search', 'dashboard', None, None),
            ],
            right_sidebar_options=[
                Option('Relative Dashboard', 'dashboard', None, None),
            ],
        )
        return context

    def get(self, request, *args, **kwargs):
        """Allows a GET."""
        self.context = self.get_context_data(**kwargs)
        dashboard_id = request.GET.get('dashboard_id')
        self.context.update(
            maternal_screening=self.maternal_screening(dashboard_id),
            show_consent_link=True if self.maternal_screening(dashboard_id)
            else self.subject_consent(dashboard_id),
            subject_consent_eligibity_link=True if self.subject_consent(dashboard_id)
            else False,
            subject_consent=self.subject_consent(dashboard_id),
        )
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        """Allows a GET."""
        self.context = self.get_context_data(**kwargs)
        return render(request, self.template_name, self.context)

    def maternal_screening(self, dashboard_id):
        try:
            return MaternalScreening.objects.get(id=dashboard_id)
        except MaternalScreening.DoesNotExist:
            return self.subject_consent(dashboard_id).maternal_screening

    def subject_consent(self, dashboard_id):
        try:
            return SubjectConsent.objects.get(id=dashboard_id)
        except SubjectConsent.DoesNotExist:
            return False
