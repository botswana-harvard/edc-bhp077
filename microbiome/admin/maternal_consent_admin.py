from django.contrib import admin

from .site import admin_site
from edc_base.modeladmin.admin import BaseModelAdmin
from microbiome.models import SubjectConsent
from microbiome.models import MaternalScreening
from microbiome.forms import SubjectConsentForm
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse


class SubjectConsentAdmin(BaseModelAdmin):

    form = SubjectConsentForm

    def reverse_next_to_dashboard(self, next_url_name, request, obj, **kwargs):
        pass

    def response_add(self, request, obj, post_url_continue=None):
        """Redirects as default unless keyword 'next' is in the GET and is a
        valid url_name (e.g. can be reversed using other GET values)."""
        http_response_redirect = super(SubjectConsent, self).response_add(request, obj, post_url_continue)
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

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#             if db_field.name == "maternal_screening":
#                 maternal_screening = MaternalScreening.objects.none()
#                 if MaternalScreening.objects.filter(id=request.GET.get('dashboard_id', 0)):
#                     maternal_screening = MaternalScreening.objects.filter(id=request.GET.get('dashboard_id', 0))
#                 kwargs["queryset"] = maternal_screening
#             return super(SubjectConsentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin_site.register(SubjectConsent, SubjectConsentAdmin)
