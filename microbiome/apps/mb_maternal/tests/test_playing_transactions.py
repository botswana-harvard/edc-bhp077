from edc_sync.tests import TestPlayTransactions

from .base_test_case import BaseTestCase


class TestMicrobiomeMbPlayTransactions(BaseTestCase, TestPlayTransactions):

    def setUp(self):
        super(TestMicrobiomeMbPlayTransactions, self).setUp()

    def populate_default_outgoing(self):
        # Maternal instances to create maternal outgoing records
        self.maternal_instances()
