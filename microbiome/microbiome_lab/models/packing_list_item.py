from django.db import models

from edc.lab.lab_packing.models import BasePackingListItem
# from edc_base.model.models import BaseUuidModel

from .aliquot import Aliquot
from .packing_list import PackingList
from .panel import Panel
from .maternal_requisition import MaternalRequisition
from .receive import Receive

from ..managers import PackingListItemManager


class PackingListItem(BasePackingListItem):

    packing_list = models.ForeignKey(PackingList, null=True)

    panel = models.ForeignKey(
        Panel,
        null=True,
        blank=True,
    )

    objects = PackingListItemManager()

    def save(self, *args, **kwargs):
        try:
            self.panel = self.maternal_requisition.panel
            self.item_datetime = self.maternal_requisition.drawn_datetime
        except AttributeError:
            pass
        super(PackingListItem, self).save(*args, **kwargs)

    @property
    def maternal_requisition(self):
        """Returns the MaternalRequisition either directly or via the
        Aliquot."""
        try:
            return MaternalRequisition.objects.get(specimen_identifier=self.item_reference)
        except MaternalRequisition.DoesNotExist:
            aliquot = Aliquot.objects.get(aliquot_identifier=self.item_reference)
            return MaternalRequisition.objects.get(
                requisition_identifier=aliquot.receive.requisition_identifier)

    @property
    def receive(self):
        """Returns an instance of Receive using the requisition_identifier or None."""
        try:
            return Receive.objects.get(requisition_identifier=self.maternal_requisition.requisition_identifier)
        except Receive.DoesNotExist:
            return None

    @property
    def drawn_datetime(self):
        """Returns the sample datetime drawn from the SubjectRequisition."""
        try:
            return self.maternal_requisition.drawn_datetime
        except AttributeError:
            return '?'

    def clinician(self):
        try:
            return self.maternal_requisition.user_created
        except AttributeError:
            return '?'

    def gender(self):
        try:
            return self.maternal_requisition.registered_subject.gender
        except AttributeError:
            return '?'

    def natural_key(self):
        return (self.item_reference, )

    class Meta:
        app_label = "microbiome_lab"
        verbose_name = 'Packing List Item'
        ordering = ('-created', )
