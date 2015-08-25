from django.contrib import admin

from ..models import InfantEligibility


@admin.register(InfantEligibility)
class InfantEligibilityAdmin(admin.ModelAdmin):

    list_display = ('maternal_enrollment_post', 'report_datetime',)

    list_filter = ('report_datetime',)
