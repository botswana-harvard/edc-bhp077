from django.utils import timezone

from django.test.testcases import TransactionTestCase

from getresults_patient.tests.factories import PatientFactory
from getresults_patient.models import Patient

from ..views import ReceiveView
from ..forms import BatchItemForm
from ..models import Batch, BatchItem


class TestBatchItemForm(TransactionTestCase):

    def setUp(self):
        self.data = {}
        self.batch_items = []
        self.batch = Batch.objects.create(item_count=3, sample_type='WB')
        self.patient = PatientFactory()

    def test_batch_item_invalid_if_no_required(self):
        batch_item_data = dict(
            protocol_number='bhp066',
            sample_type='WB',
            specimen_reference='AAA0023',
            collection_date=timezone.now().date(),
            collection_time=timezone.now().time(),
        )
        batch_item_form = BatchItemForm(data=batch_item_data)
        self.assertFalse(batch_item_form.is_valid())

    def test_batch_item_valid_if_onlyrequired(self):
        patient = PatientFactory()
        batch = Batch.objects.create(item_count=3, sample_type='WB', )
        batch_items = dict(
            tube_count=5,
            patient=patient.id,
            batch=batch.id,
            collection_date=timezone.now().date(),
            collection_time=timezone.now().time(),
            specimen_reference='ABCDSF',
            sample_type='PL'
        )
        batch_item_form = BatchItemForm(data=batch_items)
        self.assertTrue(batch_item_form.is_valid())

    def test_batch_item_valid_with_all(self):
        patient = PatientFactory()
        batch = Batch.objects.create(item_count=3, sample_type='WB', )
        batch_items = dict(
            tube_count=5,
            protocol_number='bhp066',
            patient=patient.id,
            batch=batch.id,
            sample_type='WB',
            collection_date=timezone.now().date(),
            collection_time=timezone.now().time(),
            specimen_reference='ABCDFS',
            specimen_condition='PL',
            clinician_initials='TS',
            site_code='14'
        )
        batch_item_form = BatchItemForm(data=batch_items)
        self.assertTrue(batch_item_form.is_valid())

    def test_invalid_batch_has_errormsg(self):
        patient = PatientFactory()
        batch_items = dict(
            patient=patient.id,
            colection_time=timezone.now().time(),
            collection_date=timezone.now(), sample_type='WB',
            protocol_number='bhp066')
        batch_item_form = BatchItemForm(data=batch_items)
        self.assertIn('batch', batch_item_form.errors)

    def test_batch_form_data_validates_in_view(self):
        batch = Batch.objects.create(item_count=3, sample_type='WB')
        patient = PatientFactory()
        receive = ReceiveView()
        data = dict(
            tube_count=5,
            patient=patient.id,
            batch=batch.id,
            collection_date=timezone.now().date(),
            collection_time=timezone.now().time(),
            specimen_reference='ABCDSF',
            sample_type='PL'
        )
        batch_item_form = BatchItemForm(data=data)
        batch_item_form_list = [batch_item_form.data]
        self.assertTrue(receive.validate_batch_items(batch_item_form_list))

    def test_batch(self):
        batch = Batch.objects.create(item_count=3, sample_type='WB')
        receive = ReceiveView()
        self.assertTrue(receive.batch(batch.batch_identifier))

    def test_batch_items(self):
        batch = Batch.objects.create(item_count=3, sample_type='WB')
        patient = PatientFactory()
        receive = ReceiveView()
        data = dict(
            tube_count=5,
            patient=patient.id,
            batch=batch.id,
            collection_date=timezone.now().date(),
            collection_time=timezone.now().time(),
            specimen_reference='ABCDSF',
            sample_type='PL'
        )
        batch_item_form = BatchItemForm(data=data)
        batch_items = [batch_item_form.data]
        self.assertTrue(receive.batch_items(batch_items))

    def test_create_batch_items(self):
        batch = Batch.objects.create(item_count=3, sample_type='WB')
        receive = ReceiveView()
        patient = PatientFactory()
        data = [dict(
            tube_count=5,
            patient=patient.id,
            batch=batch.id,
            collection_date=timezone.now().date(),
            collection_time=timezone.now().time(),
            specimen_reference='ABCDSF',
            sample_type='PL'
        )]
        self.assertEqual(patient.id, receive.batch_items(data)[0].patient.id)
