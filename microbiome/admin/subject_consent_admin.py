from django.contrib import admin

from microbiome.models import SubjectConsent


@admin.register(SubjectConsent)
class SubjectConsentAdmin(admin.ModelAdmin):
    pass
