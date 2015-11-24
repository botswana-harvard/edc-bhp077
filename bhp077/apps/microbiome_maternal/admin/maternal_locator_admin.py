from django.contrib import admin

from edc.subject.registration.models import RegisteredSubject
from edc_base.modeladmin.admin import BaseModelAdmin

from ..models import MaternalLocator, MaternalVisit


class MaternalLocatorAdmin(BaseModelAdmin):
    fields = ('maternal_visit',
              'registered_subject',
              'date_signed',
              'mail_address',
              'care_clinic',
              'home_visit_permission',
              'physical_address',
              'may_follow_up',
              'subject_cell',
              'subject_cell_alt',
              'subject_phone',
              'subject_phone_alt',
              'may_call_work',
              'subject_work_place',
              'subject_work_phone',
              'may_contact_someone',
              'contact_name',
              'contact_rel',
              'contact_physical_address',
              'contact_cell',
              'contact_phone',
              'has_caretaker_alt',
              'caretaker_name',
              'caretaker_cell',
              'caretaker_tel')
    list_display = ('maternal_visit',
                    'care_clinic',
                    'caretaker_name',
                    'caretaker_cell',
                    'caretaker_tel')
    list_filter = ('care_clinic', )
    search_fields = ('care_clinic', )
    radio_fields = {"home_visit_permission": admin.VERTICAL,
                    "may_follow_up": admin.VERTICAL,
                    "may_call_work": admin.VERTICAL,
                    "may_contact_someone": admin.VERTICAL,
                    'has_caretaker_alt': admin.VERTICAL, }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "maternal_visit":
                kwargs["queryset"] = MaternalVisit.objects.filter(id=request.GET.get('maternal_visit'))

        if db_field.name == "registered_subject":
            kwargs["queryset"] = RegisteredSubject.objects.filter(id__exact=request.GET.get('registered_subject', 0))
        return super(MaternalLocatorAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(MaternalLocator, MaternalLocatorAdmin)
