from collections import OrderedDict
from django.contrib import admin
from copy import copy

from edc_base.modeladmin.admin import BaseModelAdmin
from edc_export.actions import export_as_csv_action
from edc_visit_tracking.admin import VisitAdminMixin

from microbiome.apps.mb_lab.models import MaternalRequisition

from ..forms import MaternalVisitForm
from ..models import MaternalVisit


class MaternalVisitAdmin(VisitAdminMixin, BaseModelAdmin):

    form = MaternalVisitForm
    visit_attr = 'maternal_visit'
    requisition_model = MaternalRequisition
    dashboard_type = 'maternal'

    def get_fieldsets(self, request, obj=None):
        fields = copy(self.fields)
        fields.remove('information_provider')
        fields.remove('information_provider_other')
        return [(None, {'fields': fields})]

    actions = [
        export_as_csv_action(
            description="CSV Export of Maternal Visit",
            fields=[],
            delimiter=',',
            exclude=['created', 'modified', 'user_created', 'user_modified', 'revision', 'id', 'hostname_created',
                     'hostname_modified'],
            extra_fields=OrderedDict(
                {'subject_identifier': 'appointment__registered_subject__subject_identifier',
                 'gender': 'appointment__registered_subject__gender',
                 'dob': 'appointment__registered_subject__dob',
                 }),
        )]

admin.site.register(MaternalVisit, MaternalVisitAdmin)
