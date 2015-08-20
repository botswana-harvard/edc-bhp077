from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from ..models import Batch, BatchItem
from .receive_view import Option


class DisplayView(TemplateView):

    def __init__(self):
        self.context_data = dict()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.resolver_match.url_name == 'receive_user_batches':
            self.view_my_batches()
        if self.request.resolver_match.url_name == 'batch':
            self.view_batch_items()
        return super(DisplayView, self).dispatch(*args, **kwargs)

    def set_template_name(self, template):
        self.template_name = template

    def view_my_batches(self):
        self.set_template_name('my_batch.html')
        self.context_data['batches'] = Batch.objects.filter(user_created=self.request.user.username)
        self.context_data['header'] = [
            'Batch Identifier',
            'Item Count',
            'Status',
            'Protocol Number',
            'Site Code'
        ]
        return self.context_data

    def view_batch_items(self):
        self.set_template_name('batch_items.html')
        self.context_data['batch_items'] = BatchItem.objects.filter(batch__batch_identifier=self.kwargs.get('batch_identifier'))
        self.context_data['header'] = [
            'Patient',
            'Receive Datetime',
            'Specimen Reference',
            'Protocol Number',
            'Specimen Condition',
            'Sample Type'
        ]
        return self.context_data

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context.update(self.context_data)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            project_name='GETRESULTS: RECEIVE',
            section_head="",
            title='GETRESULTS RECEIVE',
            sidebar_options=[
                Option('Receive by batch', None, 'modal', '#batchModal'),
                Option('Receive single', None, 'modal', '#sampleModal'),
                Option('View my batches', 'receive_user_batches', None, None),
                Option('View all batches', '#', None, None),
                Option('Search for batch', '#', None, None),
                Option('Search for specimen', '#', None, None),
            ],
        )
        return context
