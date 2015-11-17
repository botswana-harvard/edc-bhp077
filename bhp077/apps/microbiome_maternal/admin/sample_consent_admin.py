from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc.subject.registration.models import RegisteredSubject

from bhp077.apps.microbiome_maternal.models import SampleConsent
from bhp077.apps.microbiome_maternal.forms import SampleConsentForm


class SampleConsentAdmin(BaseModelAdmin):

    dashboard_type = 'maternal'
    form = SampleConsentForm

    fields = ('registered_subject',
              'report_datetime',
              'language',
              'may_store_samples',
              'is_literate',
              'witness_name',
              'consent_benefits')
    radio_fields = {'language': admin.VERTICAL,
                    'may_store_samples': admin.VERTICAL,
                    'is_literate': admin.VERTICAL,
                    'consent_benefits': admin.VERTICAL}
    list_dispay = ('registered_subject', 'may_store_samples')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            if request.GET.get('registered_subject'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(
                    id__exact=request.GET.get('registered_subject', 0))
            else:
                self.readonly_fields = list(self.readonly_fields)
                try:
                    self.readonly_fields.index('registered_subject')
                except ValueError:
                    self.readonly_fields.append('registered_subject')
        return super(SampleConsentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SampleConsent, SampleConsentAdmin)
