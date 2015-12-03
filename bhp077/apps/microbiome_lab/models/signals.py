from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import InfantRequisition


@receiver(post_save, weak=False, dispatch_uid="infant_requisition_on_post_save")
def infant_requisition_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, InfantRequisition):
            instance.update_infantstool_metadata_on_post_save(**kwargs)
