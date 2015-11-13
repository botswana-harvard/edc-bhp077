from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin
from edc.subject.registration.models import RegisteredSubject

from bhp077.apps.microbiome_maternal.models import MaternalLabourDel

from ..models import InfantBirth
from ..forms import InfantBirthForm


class InfantBirthAdmin(BaseModelAdmin):

    form = InfantBirthForm

    list_display = (
        'registered_subject',
        'maternal_labour_del',
        'report_datetime',
        'first_name',
        'initials',
        'birth_order',
        'dob',
        'gender',
    )

    list_display = ('report_datetime', 'first_name', 'maternal_labour_del')
    list_filter = ('gender',)
    radio_fields = {'gender': admin.VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_lab_del":
            if request.GET.get('registered_subject'):
                maternal_subject_identifier = RegisteredSubject.objects.get(id=request.GET.get('registered_subject')).relative_identifier
                kwargs["queryset"] = MaternalLabourDel.objects.filter(maternal_visit__appointment__registered_subject__subject_identifier=maternal_subject_identifier)
            else:
                kwargs["queryset"] = MaternalLabourDel.objects.none()

        return super(InfantBirthAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(InfantBirth, InfantBirthAdmin)
