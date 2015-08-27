import re

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import render


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
        self.context.update(
            dashboard_id=request.GET.get('dashboard_id')
        )
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        """Allows a GET."""
        self.context = self.get_context_data(**kwargs)
        return render(request, self.template_name, self.context)

    def dashboard_id(self):
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        if not re_pk.match(self.context.get('dashboard_id') or ''):
            raise TypeError('Dashboard id must be a uuid (pk). Got {0}'.format(self.context.get('dashboard_id')))
        return self.context.get('dashboard_id')
