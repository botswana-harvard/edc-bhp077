from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc_lab.lab_requisition.admin import RequisitionAdminMixin

from microbiome.apps.mb_maternal.models import MaternalVisit

from ..models import MaternalRequisition, Panel
from ..forms import MaternalRequisitionForm


class MaternalRequisitionAdmin(RequisitionAdminMixin, BaseModelAdmin):

    dashboard_type = 'maternal'
    form = MaternalRequisitionForm
    label_template_name = 'requisition_label'
    visit_attr = 'maternal_visit'
    visit_model = MaternalVisit

    def __init__(self, *args, **kwargs):
        super(MaternalRequisitionAdmin, self).__init__(*args, **kwargs)
        for field in ['test_code', ]:
            self.fields.remove(field)

    def get_fieldsets(self, request, obj=None):
        panels = [
            'Vaginal swab (Storage)', 'Rectal swab (Storage)',
            'Skin Swab (Storage)', 'Vaginal Swab (multiplex PCR)']
        panel = Panel.objects.get(id=request.GET.get('panel'))
        if panel.name in panels:
            for field in ['estimated_volume']:
                if field in self.fields:
                    self.fields.remove(field)
        return [(None, {'fields': self.fields})]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        panel_pk = request.GET.get('panel', 0)
        if db_field.name == 'panel':
            kwargs["queryset"] = Panel.objects.filter(pk=panel_pk)
        if db_field.name == 'aliquot_type':
            if Panel.objects.filter(pk=panel_pk):
                if Panel.objects.get(pk=panel_pk).aliquot_type.all():
                    kwargs["queryset"] = Panel.objects.get(pk=panel_pk).aliquot_type.all()
        return super(MaternalRequisitionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalRequisition, MaternalRequisitionAdmin)
