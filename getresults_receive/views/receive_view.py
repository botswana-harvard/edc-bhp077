from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from ..models import Receive, Batch

from getresults_patient.models import Patient

from ..forms import BatchItemForm
from ..models import BatchItem
from ..batch_helper import BatchHelper, BatchError


class Option(object):

    def __init__(self, link_text, href, data_toggle, data_target):
        self.link_text = link_text
        self.href = href
        self.data_toggle = data_toggle
        self.data_target = data_target
        self.name = self.link_text.lower().replace(' ', '_')


class ReceiveView(TemplateView):

    template_name = 'receive.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReceiveView, self).dispatch(*args, **kwargs)

    def post(self, request):
        named_template = 'receive_batch_items.html'
        context = self.get_context_data(named_template=named_template)
        if (request.GET.get('action') and (request.GET.get('action') == ('receive' or 'draft'))):

            if request.POST.get('action') == 'receive':
                batch_items = self.batch_items_data(request)
                if not self.validate_batch_items(batch_items):
                    named_template = 'receive_batch_items.html'
                    forms = [BatchItemForm(**data) for data in batch_items]
                    context.update(batch_item_forms=forms)
                    context.update(batch_item_status=True)
                    context.update(batch_preset=False)
                else:
                    saving_status = self.save_valid_batch_items(
                        request.POST.get('batch_identifier'),
                        self.batch_items(self.batch_items_data(request))
                    )
                    context.update(message=saving_status)
                    context.update(named_template=named_template)
        return self.render_to_response(context)

    def get(self, request):
        named_template = 'receive_batch_items.html'
        context = self.get_context_data(named_template=named_template)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            project_name='GETRESULTS: RECEIVE',
            section_name="RECEIVE",
            title='GETRESULTS RECEIVE',
            sidebar_options=[
                Option('Receive by batch', None, 'modal', '#batchModal'),
                Option('Receive single', None, 'modal', '#sampleModal'),
                Option('View my batches', 'receive_user_batches', None, None),
                Option('View all batches', '#', None, None),
                Option('Search for batch', '#', None, None),
                Option('Search for specimen', '#', None, None),
            ],
            header=[
                'Identifier',
                'Patient',
                'Collected',
                'Received',
                'Type',
                'Protocol',
                'Batch'
            ],
            labels={
                'Add': 'Receive new samples',
                'View': 'View Received samples',
                'Remove': 'Remove received samples'},
            header_count=3,
            batch_present=False,
            received=Receive.objects.all(),
            received_count=Receive.objects.all().count(),
            is_batch_item_valid=False,
        )
        return context

    def field_data(self, index, request, field):
        field_data = request.POST.getlist(field, None)
        return field_data[index] if field_data else None

    def batch_items_data(self, request):
        batch_items_data = []
        for i in range(len(request.POST.getlist('patient_name', []))):
            form_field = ['patient_name', 'collect_datetime', 'rec_datetime_name', 'sample_type_name',
                          'protocol_no_name', 'site_code_name']
            _batch_items_list = []
            for field in form_field:
                _batch_items_list.append(self.field_data(i, request, field))
            batch_items_data.append(
                dict(
                    patient=_batch_items_list[0], collection_datetime=_batch_items_list[1],
                    receive_datetime=_batch_items_list[2], sample_type=_batch_items_list[3],
                    protocol_number=_batch_items_list[4], site_code=_batch_items_list[5]
                )
            )
        return batch_items_data

    def batch_items(self, batch_items_data):
        """ """
        batch_items = []
        for batch_item_data in batch_items_data:
            patient_instance = self.patient(batch_item_data.get('patient'))
            batch_instance = self.batch(batch_item_data.get('batch'))
            batch_item_data.pop('patient')
            batch_item_data.pop('batch')
            batch_item_data.update(patient=patient_instance)
            batch_item_data.update(batch=batch_instance)
            batch_item = BatchItem(**batch_item_data)
            batch_items.append(batch_item)
        return batch_items

    def save_valid_batch_items(self, batch_identifier, batch_items_data):
        batch_helper = BatchHelper(self.batch(batch_identifier))
        message = "{} Batch items successfully added".format(len(batch_items_data))
        try:
            batch_helper.save(batch_items_data)
        except BatchError as message:
            return message
        return message

    def patient(self, patient_identifier):
        patient = None
        try:
            patient = Patient.objects.get(patient_identifier=patient_identifier)
        except Patient.DoesNotExist:
            patient = Patient.objects.get(id=patient_identifier)
        return patient

    def validate_batch_items(self, batch_form_data):
        for data in batch_form_data:
            if not BatchItemForm(data=data).is_valid():
                return False
        return True

    def batch(self, batch_identifier):
        batch = None
        try:
            batch = Batch.objects.get(batch_identifier=batch_identifier)
        except Batch.DoesNotExist:
            batch = Batch.objects.get(id=batch_identifier)
        return batch
