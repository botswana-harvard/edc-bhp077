import random

from datetime import datetime

from django.test.testcases import TransactionTestCase
from django.utils import timezone

from getresults_patient.models import Patient

from ..batch_helper import BatchError, BatchHelper

from ..models import Batch, BatchItem, Receive
from getresults_receive.constants import OPEN, RECEIVED, SAVED
from getresults_receive.exceptions import AlreadyReceivedError, BatchDuplicateItemError


class TestBatch(TransactionTestCase):

    def setUp(self):
        self.batch = Batch.objects.create(
            item_count=3,
            specimen_condition='OK',
            sample_type='WB')
        self.patient = Patient.objects.create(registration_datetime=timezone.now())

    def random_string(self, length):
        return ''.join([random.choice('ABCDEFGHIJKLMNOPQRTUVWZYZ123456789') for _ in range(length)])

    def new_batch_item_instance(self, batch=None, patient=None):
        return BatchItem(
            batch=batch or self.batch,
            patient=patient or self.patient,
            protocol_number='BHP000',
            clinician_initials='MM',
            specimen_reference=self.random_string(10),
            specimen_condition='OK',
            collection_date=timezone.now(),
            collection_time=timezone.now(),
            tube_count=1,
        )

    def test_create_batch_identifier(self):
        """Test that a batch identifier is assigned when batch created"""
        prefix = datetime.today().strftime('%Y%m%d')
        self.assertTrue(self.batch.batch_identifier.startswith(prefix))

    def test_update_batch_no_change_identifier(self):
        """Test that a batch identifier does not change on update"""
        batch_id = self.batch.batch_identifier
        self.batch.save()
        self.assertEqual(batch_id, self.batch.batch_identifier)

    def test_batchitem_duplicate_raises(self):
        self.batch.item_count = 2
        items = []
        items.append(self.new_batch_item_instance())
        items.append(self.new_batch_item_instance())
        batch_helper = BatchHelper(self.batch)
        self.assertRaises(BatchDuplicateItemError, batch_helper.save, items)

    def test_batchitem_count_raises(self):
        items = []
        for _ in range(4):
            batch_item = self.new_batch_item_instance()
            items.append(batch_item)
        self.assertEqual(BatchItem.objects.all().count(), 0)
        batch_helper = BatchHelper(self.batch)
        self.assertRaises(BatchError, batch_helper.save, items)
        self.assertEqual(BatchItem.objects.all().count(), 0)

    def test_batch_receive_save(self):
        items = []
        for _ in range(3):
            items.append(self.new_batch_item_instance())
        batch_item = BatchHelper(self.batch)
        batch_item.save(items)
        self.assertEqual(BatchItem.objects.filter(batch=self.batch).count(), 3)
        batch_item.receive()
        self.assertEqual(Receive.objects.filter(batch=self.batch).count(), 3)

    def test_save_batch(self):
        items = []
        for _ in range(3):
            items.append(self.new_batch_item_instance())
        batch_helper = BatchHelper(self.batch)
        batch_helper.save(items)
        self.assertEqual(BatchItem.objects.filter(batch=self.batch).count(), 3)

    def test_save_batch_already_received(self):
        self.batch.status = RECEIVED
        self.batch.save()
        items = []
        for _ in range(3):
            items.append(self.new_batch_item_instance())
        batch_helper = BatchHelper(self.batch)
        self.assertRaises(AlreadyReceivedError, batch_helper.save, items)

    def test_batch_status_open(self):
        self.assertEqual(self.batch.status, OPEN)
        items = []
        for _ in range(3):
            items.append(self.new_batch_item_instance())
        batch_helper = BatchHelper(self.batch)
        batch_helper.save(items)
        self.assertEqual(self.batch.status, SAVED)

    def test_batch_status_received(self):
        items = []
        for _ in range(3):
            items.append(self.new_batch_item_instance())
        batch_helper = BatchHelper(self.batch)
        batch_helper.save(items)
        batch_helper.receive()
        self.assertEqual(self.batch.status, RECEIVED)
