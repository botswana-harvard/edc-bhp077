from django.contrib import admin

from .site import admin_site

from ..models import InfantEligibility


class InfantEligibilityAdmin(admin.ModelAdmin):

    list_display = ('maternal_eligibility_post', 'report_datetime',)

    list_filter = ('report_datetime',)

    radio_fields = {'infant_hiv_result': admin.VERTICAL}

admin_site.register(InfantEligibility, InfantEligibilityAdmin)
