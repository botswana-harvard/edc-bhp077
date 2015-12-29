from django.contrib import admin

from edc_lab.lab_packing.admin import BasePackingListAdmin, BasePackingListItemAdmin

from ..forms import PackingListForm, PackingListItemForm
from ..models import PackingList, PackingListItem


class PackingListAdmin(BasePackingListAdmin):

    form = PackingListForm

    fields = ('destination', 'list_items', 'list_comment',)
    list_display = ('reference', 'view_list_items', 'list_datetime',
                    'list_comment', 'destination', 'received', )
    list_filter = ('list_datetime', 'destination', 'received', 'list_comment')
    search_fields = ('id', 'list_comment')


admin.site.register(PackingList, PackingListAdmin)


class PackingListItemAdmin(BasePackingListItemAdmin):

    form = PackingListItemForm

    search_fields = ('packing_list__pk', 'packing_list__timestamp',
                     'item_description', 'item_reference', )
    list_display = ('specimen', 'priority', 'panel', 'description', 'gender',
                    'drawn_datetime', 'clinician', 'view_packing_list',
                    'received', 'received_datetime',)
    list_filter = ('created', 'panel', 'received', 'received_datetime',)


admin.site.register(PackingListItem, BasePackingListItemAdmin)
