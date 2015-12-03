from django.core.urlresolvers import reverse
from django.db import models

from edc.entry_meta_data.managers import RequisitionMetaDataManager
from edc.entry_meta_data.models import RequisitionMetaData, ScheduledEntryMetaData
from edc.lab.lab_requisition.models import BaseRequisition
from edc.subject.entry.models import LabEntry, Entry
from edc_base.audit_trail import AuditTrail
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_constants.constants import KEYED, NEW

from .aliquot_type import AliquotType
from .packing_list import PackingList
from .panel import Panel
from bhp077.apps.microbiome_infant.models import InfantVisit

from ..managers import RequisitionManager


class InfantRequisition(BaseRequisition, BaseUuidModel):

    infant_visit = models.ForeignKey(InfantVisit)

    entry_meta_data_manager = RequisitionMetaDataManager(InfantVisit)

    packing_list = models.ForeignKey(PackingList, null=True, blank=True)

    aliquot_type = models.ForeignKey(AliquotType)

    panel = models.ForeignKey(Panel)

    objects = RequisitionManager()

    history = AuditTrail()

    def get_visit(self):
        return self.infant_visit

    def get_absolute_url(self):
        return reverse('admin:microbiome_lab_infantrequisition_change', args=(self.id,))

    def aliquot(self):
        url = reverse('admin:microbiome_lab_aliquot_changelist')
        return """<a href="{url}?q={requisition_identifier}" />aliquot</a>""".format(
            url=url, requisition_identifier=self.requisition_identifier)
    aliquot.allow_tags = True

    def update_infantstool_metadata_on_post_save(self, **kwargs):
        """Changes the infant_stool_collection metadata status to NEW only if infant stool requisition is KEYED."""
        if self.infant_visit.appointment.visit_definition.code in ['2000', '2010', '2030', '2060', '2090', '2120']:
            for lab_entry in LabEntry.objects.filter(
                    requisition_panel__name='Stool storage',
                    app_label='microbiome_lab', model_name='infantrequisition'):
                requisition_meta_data = RequisitionMetaData.objects.filter(
                    appointment=self.infant_visit.appointment,
                    lab_entry=lab_entry,
                    registered_subject=self.infant_visit.appointment.registered_subject)
                if requisition_meta_data:
                    requisition_meta_data = RequisitionMetaData.objects.get(
                        appointment=self.infant_visit.appointment,
                        lab_entry=lab_entry,
                        registered_subject=self.infant_visit.appointment.registered_subject)
                    if requisition_meta_data.entry_status == KEYED:
                        entry = Entry.objects.get(
                            model_name='infantstoolcollection',
                            visit_definition_id=self.infant_visit.appointment.visit_definition_id)
                        scheduled_meta_data = ScheduledEntryMetaData.objects.filter(
                            appointment=self.infant_visit.appointment,
                            entry=entry,
                            registered_subject=self.infant_visit.appointment.registered_subject)
                        if not scheduled_meta_data:
                            scheduled_meta_data = ScheduledEntryMetaData.objects.create(
                                appointment=self.infant_visit.appointment,
                                entry=entry,
                                registered_subject=self.infant_visit.appointment.registered_subject)
                        else:
                            scheduled_meta_data = scheduled_meta_data[0]
                        scheduled_meta_data.entry_status = NEW
                        scheduled_meta_data.save()
                        return scheduled_meta_data

    class Meta:
        app_label = 'microbiome_lab'
        verbose_name = 'Infant Laboratory Requisition'
        verbose_name_plural = 'Infant Laboratory Requisition'
        unique_together = ('infant_visit', 'panel', 'is_drawn')
