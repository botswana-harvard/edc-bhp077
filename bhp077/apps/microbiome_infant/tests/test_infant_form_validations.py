from django.test import TestCase
from django import forms
from django.db import models

from ..forms import InfantStoolCollectionForm
from ..models import InfantStoolCollection


class TestInfantStoolCollectionForm(TestCase):

    def test_stool_collection_time(self):
        form = InfantStoolCollectionForm(data={'stool_colection_time': 25})
        self.assertFalse(form.is_valid())
