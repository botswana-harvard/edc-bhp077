from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.conf import settings

from ..models import Receive


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DashboardView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            project_name=self.project_name(),
            sections_head='Received',
            sections=self.sections(),
            title="Receive",
            header=[
                'Receive', 'Patient Identifier', 'Receive Identifier',
                'Collection Datetime', 'Receive Datetime', 'Sample Type', 'Protocol Number'],
            header_count=3,
            received=self.received(),
            received_count=self.received().count(),
        )
        return context

    def sections(self):
        """Override in to give a list of sections within the project"""
        return ['Order by Date Received', 'Order by Protocol', ' Received by User', 'View All Received']

    def project_name(self):
        if 'PROJECT_NAME' in dir(settings):
            return settings.PROJECT_NAME
        else:
            return ''

    def received(self):
        return Receive.objects.filter()
