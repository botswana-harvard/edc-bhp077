from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import AntenatalCallListForm
from ..models import AntenatalCallList
from ...microbiome_maternal.models import AntenatalEnrollment


class AntenatalCallListAdmin(BaseModelAdmin):

    form = AntenatalCallListForm
    date_hierarchy = 'created'
    fields = (
        "antenatal_enrollment",
        'call_attempts',
        'call_status',
        'call_outcome',
    )
    radio_fields = {'call_status': admin.VERTICAL}

    list_display = (
        'first_name',
        'initials',
        'call_attempts',
        'call_status',
        'call_outcome',
        'created',
        "consent_datetime",
        'hostname_created',
        'user_created',
    )
    list_filter = (
        'call_attempts',
        'call_status',
        'created',
        'consent_datetime',
        'hostname_created',
        'user_created',
    )

    readonly_fields = (
        'call_attempts',
        'antenatal_enrollment',
    )

    search_fields = ('antenatal_enrollment',
                     'first_name',
                     'initials')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "antenatal_enrollment":
            kwargs["queryset"] = AntenatalEnrollment.objects.filter(id__exact=request.GET.get('antenatal_enrollment', 0))
        return super(AntenatalCallListAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(AntenatalCallList, AntenatalCallListAdmin)
