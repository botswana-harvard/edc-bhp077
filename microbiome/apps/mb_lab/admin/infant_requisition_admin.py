from copy import copy

from django.contrib import admin

from edc_base.modeladmin.admin.base_model_admin import BaseModelAdmin
from edc_lab.lab_requisition.admin import RequisitionAdminMixin

from microbiome.apps.mb.constants import INFANT
from microbiome.apps.mb_infant.models import InfantVisit

from ..forms import InfantRequisitionForm
from ..models import InfantRequisition, Panel


class InfantRequisitionAdmin(RequisitionAdminMixin, BaseModelAdmin):

    dashboard_type = INFANT
    form = InfantRequisitionForm
    label_template_name = 'requisition_label'
    visit_attr = 'infant_visit'
    visit_model = InfantVisit
    panel_model = Panel

    def get_fieldsets(self, request, obj=None):
        fields = copy(self.fields)
        try:
            panel = Panel.objects.get(id=request.GET.get('panel'))
            if panel.name in ['Rectal swab (Storage)']:
                try:
                    fields.remove(fields.index('estimated_volume'))
                except ValueError:
                    pass
        except self.panel_model.DoesNotExist:
            pass
        try:
            fields.remove(fields.index('test_code'))
        except ValueError:
            pass
        return [(None, {'fields': fields})]

admin.site.register(InfantRequisition, InfantRequisitionAdmin)
