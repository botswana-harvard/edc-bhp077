from django.contrib import admin


from ..models import InfantEligibility


class InfantEligibilityAdmin(admin.ModelAdmin):

    list_display = ('maternal_eligibility_post', 'report_datetime',)

    list_filter = ('report_datetime',)

    radio_fields = {'infant_hiv_result': admin.VERTICAL}

admin.site.register(InfantEligibility, InfantEligibilityAdmin)
