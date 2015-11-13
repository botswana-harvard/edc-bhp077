from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import InfantBirth, InfantVisit


@receiver(post_save, weak=False, dispatch_uid='update_infant_registered_subject_on_post_save')
def update_infant_registered_subject_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Updates an instance of RegisteredSubject on the sender instance.

    Sender instance is a InfantBirth"""
    if not raw:
        if isinstance(instance, InfantBirth):
            instance.registered_subject.first_name = instance.first_name
            instance.registered_subject.initials = instance.initials
            instance.registered_subject.dob = instance.dob
            instance.registered_subject.gender = instance.gender
            instance.registered_subject.save(using=using)

@receiver(post_save, weak=False, dispatch_uid="infant_visit_on_post_save")
def infant_visit_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Updates maternal scheduled meta data."""
    if not raw:
        if isinstance(instance, InfantVisit):
            instance.update_scheduled_entry_meta_data()
