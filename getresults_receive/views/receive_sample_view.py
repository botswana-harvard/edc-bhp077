from django.views.generic import TemplateView
from django.conf import settings


class ReceiveSampleView(TemplateView):
    template_name = 'receive_sample.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            project_name=self.project_name(),
            sections_head='Receive Sample',
            title="Receive Sample", ),
        return context

    def project_name(self):
        if 'PROJECT_NAME' in dir(settings):
            return settings.PROJECT_NAME
        else:
            return ''
