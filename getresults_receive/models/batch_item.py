from django.db import models

from edc_base.model.models import BaseUuidModel

from getresults_patient.models import Patient

from .batch import Batch


class BatchItem(BaseUuidModel):

    batch = models.ForeignKey(Batch)

    patient = models.ForeignKey(
        Patient,
    )

    specimen_reference = models.CharField(
        max_length=25,
    )

    collection_date = models.DateField()

    collection_time = models.TimeField()

    protocol_number = models.CharField(
        verbose_name='Protocol',
        max_length=6,
        null=True,
        blank=True,
    )

    clinician_initials = models.CharField(
        verbose_name='Clinician\'s initials',
        max_length=3,
        null=True,
        blank=True,
    )

    sample_type = models.CharField(max_length=2)

    specimen_condition = models.CharField(
        max_length=2,
        null=True,
        blank=True
    )

    site_code = models.CharField(
        max_length=2,
        null=True,
        blank=True,
    )

    tube_count = models.IntegerField()

    class Meta:
        app_label = "getresults_receive"
