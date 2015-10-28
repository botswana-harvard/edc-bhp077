from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from bhp077.apps.microbiome_maternal.models import SampleConsent
from bhp077.apps.microbiome_maternal.forms import SampleConsentForm


class SampleConsentAdmin(BaseModelAdmin):

    form = SampleConsentForm

    fields = ('language',
              'may_store_samples',
              'is_literate',
              'witness_name',
              'consent_benefits')
    radio_fields = {'language': admin.VERTICAL,
                    'may_store_samples': admin.VERTICAL,
                    'is_literate': admin.VERTICAL,
                    'consent_benefits': admin.VERTICAL}

admin.site.register(SampleConsent, SampleConsentAdmin)
