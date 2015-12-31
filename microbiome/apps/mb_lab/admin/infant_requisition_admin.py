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

    def __init__(self, *args, **kwargs):
        super(InfantRequisitionAdmin, self).__init__(*args, **kwargs)
        for fld in ['test_code']:
            self.fields.remove(fld)

    def get_fieldsets(self, request, obj=None):
        panel = Panel.objects.get(id=request.GET.get('panel'))
        if panel.name in ['Rectal swab (Storage)']:
            for field in ['estimated_volume']:
                if field in self.fields:
                    self.fields.remove(field)
        return [(None, {'fields': self.fields})]

admin.site.register(InfantRequisition, InfantRequisitionAdmin)
