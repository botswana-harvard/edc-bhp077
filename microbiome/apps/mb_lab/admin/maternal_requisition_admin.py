from copy import copy

from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from lab_requisition.admin import RequisitionAdminMixin

from microbiome.apps.mb_maternal.models import MaternalVisit

from ..forms import MaternalRequisitionForm
from ..models import MaternalRequisition, Panel


class MaternalRequisitionAdmin(RequisitionAdminMixin, BaseModelAdmin):

    dashboard_type = 'maternal'
    form = MaternalRequisitionForm
    label_template_name = 'requisition_label'
    visit_attr = 'maternal_visit'
    visit_model = MaternalVisit
    panel_model = Panel

    def get_fieldsets(self, request, obj=None):
        fields = copy(self.fields)
        panel_names = [
            'Vaginal swab (Storage)',
            'Rectal swab (Storage)',
            'Skin Swab (Storage)',
            'Vaginal STI Swab (Storage)']
        panel = self.panel_model.objects.get(id=request.GET.get('panel'))
        if panel.name in panel_names:
            try:
                fields.remove(fields.index('estimated_volume'))
            except ValueError:
                pass
        try:
            fields.remove(fields.index('test_code'))
        except ValueError:
            pass
        return [(None, {'fields': self.fields})]

admin.site.register(MaternalRequisition, MaternalRequisitionAdmin)
