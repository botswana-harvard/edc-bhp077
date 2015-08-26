from django.contrib import admin

from .site import admin_site

from ..models import MaternalEligibilityPost


class MaternalEligibilityPostAdmin(admin.ModelAdmin):

    pass

admin_site.register(MaternalEligibilityPost, MaternalEligibilityPostAdmin)
