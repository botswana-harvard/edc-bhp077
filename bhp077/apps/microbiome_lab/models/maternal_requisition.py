from django.core.urlresolvers import reverse
from django.db import models

from edc.lab.lab_requisition.models import BaseRequisition
from edc_base.audit_trail import AuditTrail
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc.entry_meta_data.managers import RequisitionMetaDataManager

from bhp077.apps.microbiome_maternal.models import MaternalVisit

from ..managers import RequisitionManager

from .aliquot_type import AliquotType
from .packing_list import PackingList
from .panel import Panel


class MaternalRequisition(BaseRequisition, BaseUuidModel):

    maternal_visit = models.ForeignKey(MaternalVisit)

    packing_list = models.ForeignKey(PackingList, null=True, blank=True)

    aliquot_type = models.ForeignKey(AliquotType)

    panel = models.ForeignKey(Panel)

    objects = RequisitionManager()

    history = AuditTrail()

    entry_meta_data_manager = RequisitionMetaDataManager(MaternalVisit)

    def __unicode__(self):
        return '{0} {1}'.format(unicode(self.panel), self.requisition_identifier)

    def get_visit(self):
        return self.maternal_visit

    def natural_key(self):
        return (self.requisition_identifier,)

    def aliquot(self):
        url = reverse('admin:microbiome_lab_aliquot_changelist')
        return """<a href="{url}?q={requisition_identifier}" />aliquot</a>""".format(
            url=url, requisition_identifier=self.requisition_identifier)
    aliquot.allow_tags = True

    def dashboard(self):
        url = reverse(
            'subject_dashboard_url',
            kwargs={
                'dashboard_type': self.maternal_visit.appointment.registered_subject.subject_type.lower(),
                'dashboard_model': 'appointment',
                'dashboard_id': self.maternal_visit.appointment.pk,
                'show': 'appointments'})
        return """<a href="{url}" />dashboard</a>""".format(url=url)
    dashboard.allow_tags = True

    class Meta:
        app_label = 'microbiome_lab'
        verbose_name = 'Maternal Requisition'
        verbose_name_plural = 'Maternal Requisition'
        unique_together = ('maternal_visit', 'panel', 'is_drawn')
        ordering = ('-created', )
