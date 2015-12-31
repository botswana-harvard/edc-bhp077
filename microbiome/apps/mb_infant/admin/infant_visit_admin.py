from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc_visit_tracking.admin import VisitAdminMixin

from microbiome.apps.mb.constants import INFANT
from microbiome.apps.mb_lab.models import InfantRequisition

from ..forms import InfantVisitForm
from ..models import InfantVisit


class InfantVisitAdmin(VisitAdminMixin, BaseModelAdmin):

    form = InfantVisitForm
    dashboard_type = INFANT
    requisition_model = InfantRequisition
    visit_attr = 'infant_visit'

admin.site.register(InfantVisit, InfantVisitAdmin)
