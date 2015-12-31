from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc_visit_tracking.admin import VisitAdminMixin

from microbiome.apps.mb_lab.models import MaternalRequisition

from ..forms import MaternalVisitForm
from ..models import MaternalVisit


class MaternalVisitAdmin(VisitAdminMixin, BaseModelAdmin):

    form = MaternalVisitForm
    visit_attr = 'maternal_visit'
    requisition_model = MaternalRequisition
    dashboard_type = 'maternal'

admin.site.register(MaternalVisit, MaternalVisitAdmin)
