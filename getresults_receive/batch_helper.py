from django.db import IntegrityError, transaction
from django.utils import timezone

from .constants import SAVED, OPEN, RECEIVED
from .exceptions import BatchError, BatchReceiveError, BatchSaveError, AlreadyReceivedError
from .models import BatchItem, Receive


class BatchHelper(object):

    def __init__(self, batch):
        self.batch = batch

    def save(self, items):
        """Saves the items to the BatchItem model or rollsback and raises an exception."""
        if self.batch.status == RECEIVED:
            raise AlreadyReceivedError('Batch {} is already received.'.format(self.batch.batch_identifier))
        self.validate_count(items)
        try:
            with transaction.atomic():
                for item in items:
                    item.save()
            self.batch.status = SAVED
            self.batch.save()
        except IntegrityError as e:
            raise BatchSaveError(str(e))

    def receive(self):
        """Saves batch to the Receive model or raises an exception."""
        if self.batch.status == RECEIVED:
            raise AlreadyReceivedError('Batch {} is already received.'.format(self.batch.batch_identifier))
        elif self.batch.status == OPEN:
            raise BatchSaveError('Batch {} has not been saved.'.format(self.batch.batch_identifier))
        elif self.batch.status == SAVED:
            try:
                with transaction.atomic():
                    for batch_item in BatchItem.objects.filter(batch=self.batch):
                        receive = Receive(
                            batch=self.batch,
                            patient=batch_item.patient,
                            receive_datetime=timezone.now(),
                            collection_date=batch_item.collection_date,
                            collection_time=batch_item.collection_time,
                            protocol_number=batch_item.protocol_number,
                            clinician_initials=batch_item.clinician_initials,
                            specimen_condition=batch_item.specimen_condition,
                            sample_type=batch_item.sample_type,
                            site_code=batch_item.site_code,
                            tube_count=batch_item.tube_count,
                        )
                        receive.save()
                self.batch.status = RECEIVED
                self.batch.save()
            except IntegrityError as e:
                raise BatchReceiveError(str(e))
        else:
            raise BatchError('Unknown status for batch {}. Got {}'.format(self.batch, self.batch.status))

    def validate_count(self, items):
        """Raises an exception id item count does not match batch."""
        if len(items) != self.batch.item_count:
            raise BatchError('Expected {} items. Got {}'.format(self.batch.item_count, len(items)))
