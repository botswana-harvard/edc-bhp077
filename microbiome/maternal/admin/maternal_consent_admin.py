from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect

from edc_base.modeladmin.admin import BaseModelAdmin

from microbiome.maternal.forms import MaternalConsentForm
from microbiome.maternal.models import MaternalConsent


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

    def reverse_next_to_dashboard(self, next_url_name, request, obj, **kwargs):
        pass

    def response_add(self, request, obj, post_url_continue=None):
        """Redirects as default unless keyword 'next' is in the GET and is a
        valid url_name (e.g. can be reversed using other GET values)."""
        http_response_redirect = super(MaternalConsent, self).response_add(request, obj, post_url_continue)
        custom_http_response_redirect = None
        if '_addanother' not in request.POST and '_continue' not in request.POST:
            if request.GET.get('next'):
                custom_http_response_redirect = self.response_add_redirect_on_next_url(
                    request.GET.get('next'),
                    request,
                    obj,
                    post_url_continue,
                    post_save=request.POST.get('_save'),
                    post_save_next=request.POST.get('_savenext'),
                    post_cancel=request.POST.get('_cancel'))
        return custom_http_response_redirect or http_response_redirect

    def response_add_redirect_on_next_url(
            self, next_url_name, request, obj, post_url_continue, post_save=None,
            post_save_next=None, post_cancel=None):
            url = ('{0}?dashboard_id={1}').format(reverse('dashboard_id_url', kwargs={'dashboard_id': obj.id}), obj.id)
            return HttpResponseRedirect(url)

admin.site.register(MaternalConsent, MaternalConsentAdmin)
