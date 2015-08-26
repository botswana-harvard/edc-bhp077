from django.contrib import admin

from ..models import MaternalEligibilityPre


@admin.register(MaternalEligibilityPre)
class MaternalEligibilityPreAdmin(admin.ModelAdmin):

    fields = (
        'report_datetime',
        'first_name',
        'initials',
        'dob',
        'gender',
        'has_identity',
        'citizen',
        'disease',
        'currently_pregnant',
        'pregnancy_weeks',
        'verbal_hiv_status',
        'evidence_pos_hiv_status',
        'rapid_test_result',
    )
