from django.test import TransactionTestCase

from ..forms import BatchForm


class TestBatchForm(TransactionTestCase):

    def setUp(self):
        self.data = {}

    def test_batch_valid(self):
        self.data = dict(item_count=5, status='done')
        batch_form = BatchForm(data=self.data)
        self.assertTrue(batch_form.is_valid())
