from django.contrib import admin

from .site import admin_site
from edc_base.modeladmin.admin import BaseModelAdmin
from microbiome.models import SubjectConsent


class SubjectConsentAdmin(BaseModelAdmin):

    pass

admin_site.register(SubjectConsent, SubjectConsentAdmin)
