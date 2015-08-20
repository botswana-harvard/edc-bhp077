from django.contrib import admin

from .models import Receive, Batch, BatchItem

from getresults.admin import admin_site


class ReceiveAdmin(admin.ModelAdmin):

    date_hierarchy = 'receive_datetime'

    list_display = ('receive_identifier', 'receive_datetime', 'protocol_number', 'batch')
    list_filter = ('receive_datetime', 'protocol_number')
    search_fields = ('receive_datetime', 'protocol_number',)
admin_site.register(Receive, ReceiveAdmin)


class BatchAdmin(admin.ModelAdmin):
    model = Batch
admin_site.register(Batch, BatchAdmin)


class BatchItemAdmin(admin.ModelAdmin):
    model = BatchItem
admin_site.register(BatchItem, BatchItemAdmin)
