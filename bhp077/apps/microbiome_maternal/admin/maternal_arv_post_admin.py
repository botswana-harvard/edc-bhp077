from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseTabularInline
from ..forms import MaternalArvPostForm, MaternalArvPostModForm, MaternalArvPostAdhForm
from ..models import MaternalVisit, MaternalArvPost, MaternalArvPostMod, MaternalArvPostAdh


class MaternalArvPostModInlineAdmin(BaseTabularInline):

    model = MaternalArvPostMod
    form = MaternalArvPostModForm
    extra = 1


class MaternalArvPostModAdmin(BaseModelAdmin):

    form = MaternalArvPostModForm
    list_display = ('maternal_arv_post', 'arv_code', 'dose_status', 'modification_date', 'modification_code')

    radio_fields = {
        "arv_code": admin.VERTICAL,
        "dose_status": admin.VERTICAL,
        "modification_code": admin.VERTICAL,
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_arv_post":
            if request.GET.get('maternal_visit'):
                infant_visit = MaternalVisit.objects.get(id=request.GET.get('maternal_visit'))
                kwargs["queryset"] = MaternalArvPostAdh.objects.filter(registered_subject=infant_visit.appointment.registered_subject)
        return super(MaternalArvPostAdhAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalArvPostMod, MaternalArvPostModAdmin)


class MaternalArvPostAdmin(BaseModelAdmin):

    form = MaternalArvPostForm

    fields = (
        "maternal_visit",
        "haart_last_visit",
        "haart_reason",
        "haart_reason_other",
        "arv_status")

    radio_fields = {
        "haart_last_visit": admin.VERTICAL,
        "haart_reason": admin.VERTICAL,
        "arv_status": admin.VERTICAL}
    inlines = [MaternalArvPostModInlineAdmin, ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
            if request.GET.get('maternal_visit'):
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        return super(MaternalArvPostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalArvPost, MaternalArvPostAdmin)


class MaternalArvPostAdhAdmin(BaseModelAdmin):

    form = MaternalArvPostAdhForm
    fields = (
        "maternal_visit",
        "maternal_arv_post",
        "missed_doses",
        "missed_days",
        "missed_days_discnt",
        "comment")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))
        if db_field.name == "maternal_arv_post":
            if request.GET.get('maternal_visit'):
                infant_visit = MaternalVisit.objects.get(id=request.GET.get('maternal_visit'))
                kwargs["queryset"] = MaternalArvPostAdh.objects.filter(registered_subject=infant_visit.appointment.registered_subject)
        return super(MaternalArvPostAdhAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MaternalArvPostAdh, MaternalArvPostAdhAdmin)
