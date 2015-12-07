from django.db.models.signals import post_save
from django.dispatch import receiver

from edc_constants.constants import NEW
from edc.entry_meta_data.models import ScheduledEntryMetaData
from edc.subject.entry.models import Entry

from ..models import InfantBirth, InfantVisit
from bhp077.apps.microbiome_maternal.models.maternal_visit import MaternalVisit
from bhp077.apps.microbiome_maternal.models.postnatal_enrollment import PostnatalEnrollment


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


@receiver(post_save, weak=False, dispatch_uid="create_additional_maternal_forms_entry_meta_data")
def create_additional_maternal_forms_entry_meta_data(sender, instance, raw, created, using, **kwargs):
    """Inspects the InfantVisit and deletes infant's meta data for the visit if off study
    or infant death."""
    if not raw:
        if isinstance(instance, InfantVisit):
            if instance.reason == 'off study':
                entry = Entry.objects.get(
                    model_name='infantoffstudy',
                    visit_definition_id=instance.appointment.visit_definition_id)
                scheduled_meta_data = ScheduledEntryMetaData.objects.filter(
                    appointment=instance.appointment,
                    entry=entry,
                    registered_subject=instance.appointment.registered_subject)
                if not scheduled_meta_data:
                    scheduled_meta_data = ScheduledEntryMetaData.objects.create(
                        appointment=instance.appointment,
                        entry=entry,
                        registered_subject=instance.appointment.registered_subject)
                else:
                    scheduled_meta_data = scheduled_meta_data[0]
                scheduled_meta_data.entry_status = NEW
                scheduled_meta_data.save()
            if instance.reason == 'death':
                entries = Entry.objects.filter(
                    model_name__in=['infantdeath', 'infantoffstudy'],
                    visit_definition_id=instance.appointment.visit_definition_id)
                for entry in entries:
                    scheduled_meta_data = ScheduledEntryMetaData.objects.filter(
                        appointment=instance.appointment,
                        entry=entry[0],
                        registered_subject=instance.appointment.registered_subject)
                    if not scheduled_meta_data:
                        scheduled_meta_data = ScheduledEntryMetaData.objects.create(
                            appointment=instance.appointment,
                            entry=entry[0],
                            registered_subject=instance.appointment.registered_subject)
                    else:
                        scheduled_meta_data = scheduled_meta_data[0]
                    scheduled_meta_data.entry_status = NEW
                    scheduled_meta_data.save()
