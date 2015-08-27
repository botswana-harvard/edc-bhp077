from django.contrib import admin

from .site import admin_site
from edc_base.modeladmin.admin import BaseModelAdmin
from microbiome.models import SubjectConsent
from microbiome.models import MaternalScreening
from microbiome.forms import SubjectConsentForm


class SubjectConsentAdmin(BaseModelAdmin):

    form = SubjectConsentForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
            if db_field.name == "maternal_screening":
                maternal_screening = MaternalScreening.objects.none()
                if MaternalScreening.objects.filter(id=request.GET.get('dashboard_id', 0)):
                    maternal_screening = MaternalScreening.objects.filter(id=request.GET.get('dashboard_id', 0))
                kwargs["queryset"] = maternal_screening
            return super(SubjectConsentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin_site.register(SubjectConsent, SubjectConsentAdmin)
