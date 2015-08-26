from django.contrib import admin

from .site import admin_site

from microbiome.models import SubjectConsent


class SubjectConsentAdmin(admin.ModelAdmin):

    pass

admin_site.register(SubjectConsent, SubjectConsentAdmin)
