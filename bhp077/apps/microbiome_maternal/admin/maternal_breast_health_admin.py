from django.contrib import admin

from ..forms import MaternalBreastHealthForm
from ..models import MaternalBreastHealth

from .base_maternal_model_admin import BaseMaternalModelAdmin


class MaternalBreastHealthAdmin(BaseMaternalModelAdmin):

    form = MaternalBreastHealthForm

    radio_fields = {
        "breast_feeding": admin.VERTICAL,
        "has_mastitis": admin.VERTICAL,
        "mastitis": admin.VERTICAL,
        "has_lesions": admin.VERTICAL,
        "lesions": admin.VERTICAL,
        "told_stop_bf": admin.VERTICAL,
    }
admin.site.register(MaternalBreastHealth, MaternalBreastHealthAdmin)
