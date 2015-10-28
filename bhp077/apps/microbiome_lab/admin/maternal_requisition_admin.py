from django.contrib import admin

from edc.lab.lab_requisition.admin import BaseRequisitionModelAdmin
from edc.export.actions import export_as_csv_action

from apps.microbiome_maternal.models import MaternalVisit

from ..actions import print_requisition_label
from ..models import MaternalRequisition, Panel
from ..forms import MaternalRequisitionForm


class MaternalRequisitionAdmin(BaseRequisitionModelAdmin):

    visit_model = MaternalVisit
    visit_attr = 'maternal_visit'

    def __init__(self, *args, **kwargs):
        super(MaternalRequisitionAdmin, self).__init__(*args, **kwargs)
        self.list_filter = list(self.list_filter)
        self.list_filter = tuple(self.list_filter)

    form = MaternalRequisitionForm
    visit_model = MaternalVisit
    visit_fieldname = 'maternal_visit'
    dashboard_type = 'maternal'

    label_template_name = 'requisition_label'
    actions = [print_requisition_label,
               export_as_csv_action("Export as csv", fields=[], delimiter=',', exclude=['id', 'revision',
                                                                                        'hostname_created',
                                                                                        'hostname_modified',
                                                                                        'user_created',
                                                                                        'user_modified'],)]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        panel_pk = request.GET.get('panel', 0)
        if db_field.name == 'panel':
            kwargs["queryset"] = Panel.objects.filter(pk=panel_pk)
        if db_field.name == 'aliquot_type':
            if Panel.objects.filter(pk=panel_pk):
                if Panel.objects.get(pk=panel_pk).aliquot_type.all():
                    kwargs["queryset"] = Panel.objects.get(pk=panel_pk).aliquot_type.all()
        return super(BaseRequisitionModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalRequisition, MaternalRequisitionAdmin)
