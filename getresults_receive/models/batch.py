from django.db import models
from django.utils import timezone

from edc_base.model.models import BaseUuidModel
from getresults_identifier.batch_identifier import BatchIdentifier


class Batch(BaseUuidModel):

    batch_identifier = models.CharField(
        max_length=25,
        null=True,
        editable=False,
    )

    batch_datetime = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )

    receive_datetime = models.DateTimeField(
        null=True,
        editable=False,
    )

    status = models.CharField(
        max_length=10,
        default='Open',
        editable=False,
    )

    item_count = models.IntegerField(
        default=1,
    )

    sample_type = models.CharField(
        max_length=2,
        null=True,
        blank=True,
    )

    protocol_number = models.CharField(
        max_length=5,
        null=True,
        blank=True
    )

    specimen_condition = models.CharField(
        max_length=2,
        null=True,
        blank=True
    )

    site_code = models.CharField(
        max_length=2,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.batch_identifier = BatchIdentifier().identifier
        super().save(*args, **kwargs)

    class Meta:
        app_label = "getresults_receive"
