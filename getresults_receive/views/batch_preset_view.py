from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from ..models import Batch

from ..forms import BatchForm
from django.contrib import messages


class BatchPresetView(TemplateView):
    template_name = 'receive.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BatchPresetView, self).dispatch(*args, **kwargs)

    def get(self, request, **kwargs):
        context = self.get_context_data()
        context.update(named_template='receive_batch_items.html')
        return self.render_to_response(context)

    def post(self, request):
        context = self.get_context_data()
        form = BatchForm(request.POST)
        if form.is_valid():
            item_count = form.cleaned_data.get('item_count')
            collection_date = form.cleaned_data.get('collection_date')
            sample_type = form.cleaned_data.get('sample_type')
            protocol_no = form.cleaned_data.get('protocol_no')
            site_code = form.cleaned_data.get('site_code')
            batch = None
            try:
                batch = Batch(
                    item_count=item_count,
                    sample_type=sample_type,
                    protocol_number=protocol_no,
                    site_code=site_code,
                    user_created=request.user.username,
                )
                batch.save()
            except Exception as err:
                print(err)
                batch = Batch.objects.first()
            context.update(
                collection_date_name=collection_date.strftime("%Y-%m-%d") if collection_date else '',
                sample_type_name=sample_type,
                protocol_no_name=protocol_no,
                site_code_name=site_code,
                batch_size=range(0, item_count),
                named_template='receive_batch_items.html',
                batch_identifier=batch.batch_identifier,
                batch_preset=True,
            )
            return self.render_to_response(context)
        else:
            message = ''
            context.update(preset_form=form)
            context.update(batch_error='failed')
            context.update(named_template='receive_batch_items.html')
            messages.add_message(request, messages.INFO, message)
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            sections_head='Receive Batch',
            batch_preset=True,
            title="Receive Batch"
        )
        return context
