from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from bhp077.apps.microbiome_maternal.forms import MaternalConsentForm
from bhp077.apps.microbiome_maternal.models import MaternalConsent


class MaternalConsentAdmin(BaseModelAdmin):

    form = MaternalConsentForm

    fields = ('first_name',
              'last_name',
              'initials',
              'language',
              'is_literate',
              'witness_name',
              'consent_datetime',
              'gender',
              'dob',
              'guardian_name',
              'is_dob_estimated',
              'citizen',
              'identity',
              'identity_type',
              'confirm_identity',
              'comment')
    radio_fields = {'citizen': admin.VERTICAL,
                    'language': admin.VERTICAL,
                    'is_literate': admin.VERTICAL,
                    'gender': admin.VERTICAL,
                    'is_dob_estimated': admin.VERTICAL,
                    'identity_type': admin.VERTICAL}
    list_display = ('subject_identifier',
                    'is_verified',
                    'is_verified_datetime',
                    'first_name',
                    'initials',
                    'gender',
                    'dob',
                    'consent_datetime',
                    'created',
                    'modified',
                    'user_created',
                    'user_modified')

admin.site.register(MaternalConsent, MaternalConsentAdmin)
