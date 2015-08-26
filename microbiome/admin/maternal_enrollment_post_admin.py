from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from ..forms import MaternalEnrollmentPostForm
from ..models import MaternalEnrollmentPost
from .site import admin_site


@admin.register(MaternalEnrollmentPost)
class MaternalEnrollmentPostAdmin(BaseModelAdmin):
    form = MaternalEnrollmentPostForm
admin_site.register(MaternalEnrollmentPost, MaternalEnrollmentPostAdmin)
