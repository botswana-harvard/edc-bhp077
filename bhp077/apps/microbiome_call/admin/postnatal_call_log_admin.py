from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseStackedInline

from ..forms import PostnatalCallLogForm, PostnatalCallLogEntryForm
from ..models import PostnatalCallLog, PostnatalCallLogEntry
from ..models import PostnatalCallList


class PostnatalCallLogEntryAdminInline(BaseStackedInline):
    instructions = [
        'Please read out to participant. "We hope you have been well since our visit last year. '
        'As a member of this study, it is time for your revisit in which we will ask you '
        'some questions and perform some tests."',
        'Please read out to contact other than participant. (Note: You may NOT disclose that the '
        'participant is a member of the Microbiome study). "We would like to contact a participant '
        '(give participant name) who gave us this number as a means to contact them. Do you know '
        'how we can contact this person directly? This may be a phone number or a physical address.']

    form = PostnatalCallLogEntryForm
    model = PostnatalCallLogEntry
    max_num = 3
    extra = 1

    fields = (
        'call_datetime',
        'invalid_numbers',
        'contact_type',
        'time_of_week',
        'time_of_day',
        'appt',
        'appt_date',
        'appt_grading',
        'appt_location',
        'appt_location_other',
        'call_again',
    )

    radio_fields = {
        "contact_type": admin.VERTICAL,
        "time_of_week": admin.VERTICAL,
        "time_of_day": admin.VERTICAL,
        "appt": admin.VERTICAL,
        "appt_grading": admin.VERTICAL,
        "appt_location": admin.VERTICAL,
        "call_again": admin.VERTICAL,
    }


class PostnatalCallLogAdmin(BaseModelAdmin):

    instructions = [
        '<h5>Please read out to participant:</h5> "We hope you have been well since our visit last year. '
        'As a member of this study, it is time for your revisit in which we will ask you '
        'some questions and perform some tests."',
        '<h5>Please read out to contact other than participant:</h5> (<B>IMPORTANT:</B> You may NOT disclose that the '
        'participant is a member of the Microbiome study).<BR>"We would like to contact a participant '
        '(give participant name) who gave us this number as a means to contact them. Do you know '
        'how we can contact this person directly? This may be a phone number or a physical address.']

    form = PostnatalCallLogForm

    fields = ("postnatal_call_list", 'locator_information', 'contact_notes')

    inlines = [PostnatalCallLogEntryAdminInline, ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "antenatal_call_list":
            kwargs["queryset"] = PostnatalCallList.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(PostnatalCallLogAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(PostnatalCallLog, PostnatalCallLogAdmin)


class PostnatalCallLogEntryAdmin(BaseModelAdmin):

    date_hierarchy = 'appt_date'
    instructions = [
        'Please read out to participant. "We hope you have been well since our visit last year. '
        'As a member of this study, it is time for your revisit in which we will ask you '
        'some questions and perform some tests."',
        'Please read out to contact other than participant. (Note: You may NOT disclose that the '
        'participant is a member of the Microbiome study). "We would like to contact a participant '
        '(give participant name) who gave us this number as a means to contact them. Do you know '
        'how we can contact this person directly? This may be a phone number or a physical address.']

    form = PostnatalCallLogEntryForm
    fields = (
        'postnatal_call_log',
        'call_datetime',
        'invalid_numbers',
        'contact_type',
        'time_of_week',
        'time_of_day',
        'appt',
        'appt_date',
        'appt_grading',
        'appt_location',
        'appt_location_other',
        'call_again',
    )

    radio_fields = {
        "contact_type": admin.VERTICAL,
        "time_of_week": admin.VERTICAL,
        "time_of_day": admin.VERTICAL,
        "appt": admin.VERTICAL,
        "appt_grading": admin.VERTICAL,
        "appt_location": admin.VERTICAL,
        "call_again": admin.VERTICAL,
    }

    list_display = (
        'postnatal_call_log',
        'call_datetime',
        'appt',
        'appt_date',
        'call_again',
    )

    list_filter = (
        'call_datetime',
        'appt',
        'appt_date',
        'call_again',
        'created',
        'modified',
        'hostname_created',
        'hostname_modified',
    )

    search_fields = ('antenatal_call_log__antenatal_call_list__first_name', 'id')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "postnatal_call_log":
            kwargs["queryset"] = PostnatalCallLog.objects.filter(id__exact=request.GET.get('postnatal_call_log', 0))
        return super(PostnatalCallLogEntryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(PostnatalCallLogEntry, PostnatalCallLogEntryAdmin)
