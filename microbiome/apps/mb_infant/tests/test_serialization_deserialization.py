from edc_sync.tests import TestSerializeDeserialize

from .base_test_case import BaseTestCase


class TestSerializationDeserialization(BaseTestCase, TestSerializeDeserialize):

    def setUp(self):
        super(TestSerializationDeserialization, self).setUp()

    def get_model_instances(self):
        return self.infant_instances()
