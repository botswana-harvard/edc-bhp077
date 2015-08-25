from django.contrib import admin

from ..models import MaternalEligibilityPre


@admin.register(MaternalEligibilityPre)
class MaternalEligibilityPreAdmin(admin.ModelAdmin):
    pass
