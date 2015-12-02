from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import PostnatalCallListForm
from ..models import PostnatalCallList
from ...microbiome_maternal.models import PostnatalEnrollment


class PostnatalCallListAdmin(BaseModelAdmin):

    form = PostnatalCallListForm
    date_hierarchy = 'created'
    fields = (
        "postnatal_enrollment",
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
        'postnatal_enrollment',
    )

    search_fields = ('postnatal_enrollment',
                     'first_name',
                     'initials')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "postnatal_enrollment":
            kwargs["queryset"] = PostnatalEnrollment.objects.filter(id__exact=request.GET.get('postnatal_enrollment', 0))
        return super(PostnatalCallListAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(PostnatalCallList, PostnatalCallListAdmin)
