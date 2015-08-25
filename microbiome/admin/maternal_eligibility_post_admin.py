from django.contrib import admin

from ..models import MaternalEligibilityPost


@admin.register(MaternalEligibilityPost)
class MaternalEligibilityPostPreAdmin(admin.ModelAdmin):
    pass
