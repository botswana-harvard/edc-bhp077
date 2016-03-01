from edc_sync.tests import TestPlayTransactions

from .base_test_case import BaseTestCase


class TestMicrobiomeInfPlayTransactions(BaseTestCase, TestPlayTransactions):

    def setUp(self):
        super(TestMicrobiomeInfPlayTransactions, self).setUp()

    def populate_default_outgoing(self):
        # Infant instances to create maternal outgoing records
        self.infant_instances()
