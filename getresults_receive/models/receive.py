from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models
from django.db.models import get_model
from django.utils import timezone

from edc_base.model.models import BaseUuidModel, HistoricalRecords

from getresults_patient.models import Patient

from .batch import Batch
from .identifiers import ReceiveIdentifier


class Receive(BaseUuidModel):

    receive_identifier = models.CharField(
        max_length=25,
        editable=False,
        unique=True
    )

    batch = models.ForeignKey(Batch)

    patient = models.ForeignKey(Patient)

    receive_datetime = models.DateTimeField(
        default=timezone.now
    )

    specimen_reference = models.CharField(
        max_length=25,
        null=True,
        blank=True,
    )

    collection_date = models.DateField()

    collection_time = models.TimeField()

    protocol_number = models.CharField(
        verbose_name='Protocol',
        max_length=6,
    )

    clinician_initials = models.CharField(
        verbose_name='Clinician\'s initials',
        max_length=3,
    )

    specimen_condition = models.CharField(
        max_length=2,
    )

    sample_type = models.CharField(
        max_length=2,
    )

    site_code = models.CharField(
        max_length=2,
        null=True,
        blank=True,
    )

    tube_count = models.IntegerField()

    history = HistoricalRecords()

    def __str__(self):
        return '{}: {}'.format(
            self.receive_identifier, self.receive_datetime.strftime('%Y-%m-%d %H:%M'))

    def save(self, *args, **kwargs):
        if not self.id and not self.receive_identifier:
            self.receive_identifier = ReceiveIdentifier().identifier
        super(Receive, self).save(*args, **kwargs)

    class Meta:
        app_label = 'getresults_receive'
        db_table = 'getresults_receive'
        unique_together = (
            ('protocol_number', 'patient', 'collection_date', 'collection_time', 'sample_type', 'tube_count', ))

    def create_aliquot(self, instance):
        """Create an aliquote."""
        aliquot_model = get_model('getresults_aliquot', 'Aliquot')
        aliquot_type_model = get_model('getresults_aliquot', 'AliquotType')
        # Aliquote type will be queried by sample type on receive
        if aliquot_type_model.objects.filter(name='whole blood', alpha_code='WB', numeric_code='02').exists():
            aliquot_type = aliquot_type_model.objects.get(name='whole blood', alpha_code='WB', numeric_code='02')
        else:
            aliquot_type = aliquot_type_model.objects.create(name='whole blood', alpha_code='WB', numeric_code='02')
        try:
            aliquot_model.objects.create(
                receive=instance,
                aliquot_type=aliquot_type
            )
        except:
            pass


@receiver(post_save, weak=False, dispatch_uid='create_aliquot_on_post_save')
def create_aliquot_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Creates and aliquot after a sample is received."""
    if not raw:
        if isinstance(instance, Receive):
            if created:
                try:
                    instance.create_aliquot(instance)
                except AttributeError:
                    pass
