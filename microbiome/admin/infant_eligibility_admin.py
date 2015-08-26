from django.contrib import admin

from .site import admin_site

from ..models import InfantEligibility


class InfantEligibilityAdmin(admin.ModelAdmin):

    list_display = ('maternal_enrollment_post', 'report_datetime',)

    list_filter = ('report_datetime',)

admin_site.register(InfantEligibility, InfantEligibilityAdmin)
