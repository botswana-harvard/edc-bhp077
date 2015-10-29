from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc.subject.registration.models import RegisteredSubject

from bhp077.apps.microbiome_maternal.forms import MaternalConsentForm
from bhp077.apps.microbiome_maternal.models import MaternalConsent


class MaternalConsentAdmin(BaseModelAdmin):

    form = MaternalConsentForm

    fields = ('registered_subject',
              'first_name',
              'last_name',
              'initials',
              'language',
              'is_literate',
              'witness_name',
              'consent_datetime',
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
                    'is_dob_estimated': admin.VERTICAL,
                    'identity_type': admin.VERTICAL}
    list_display = ('subject_identifier',
                    'registered_subject',
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
        return super(MaternalConsentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalConsent, MaternalConsentAdmin)
