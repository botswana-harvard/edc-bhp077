from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData
from edc.subject.entry.models import Entry, LabEntry
from edc.subject.appointment.models import Appointment
from django.core.exceptions import MultipleObjectsReturned


class MetaDataMixin(object):
    def meta_data_visit_unshceduled(self, appointment):
        meta_data = self.query_scheduled_meta_data(appointment, appointment.registered_subject)
        self.remove_scheduled_forms(meta_data)

    def remove_scheduled_forms(self, scheduled_meta_data):
        # Ensure there are no keyed forms
        for meta_data in scheduled_meta_data:
            if meta_data.entry_status == 'KEYED':
                return False
        scheduled_meta_data.delete()
        return True

    def remove_scheduled_requisition(self, lab_meta_data):
        # Ensure there are no keyed forms
        for meta_data in lab_meta_data:
            if meta_data.entry_status == 'KEYED':
                return False
        lab_meta_data.delete()
        return True

    def query_entry(self, model_name, visit_definition):
        return Entry.objects.get(model_name=model_name, visit_definition=visit_definition)

    def query_scheduled_meta_data(self, appointment, registered_subject, entry=None):
        try:
            return ScheduledEntryMetaData.objects.get(
                appointment=appointment, registered_subject=registered_subject, entry=entry)
        except ScheduledEntryMetaData.DoesNotExist, MultipleObjectsReturned:
            return ScheduledEntryMetaData.objects.filter(appointment=appointment, registered_subject=registered_subject)

    def query_requisition_meta_data(self, appointment, registered_subject, lab_entry=None):
        try:
            return RequisitionMetaData.objects.get(
                appointment=appointment, lab_entry=lab_entry, registered_subject=registered_subject)
        except RequisitionMetaData.DoesNotExist, MultipleObjectsReturned:
            return RequisitionMetaData.objects.filter(appointment=appointment, registered_subject=registered_subject)

    def create_scheduled_meta_data(self, appointment, entry, registered_subject):
        appointment = self.check_instance(appointment)
        scheduled_meta_data = self.query_scheduled_meta_data(appointment, entry, registered_subject)
        if not scheduled_meta_data:
            scheduled_meta_data = ScheduledEntryMetaData.objects.create(appointment=appointment, entry=entry, registered_subject=registered_subject)
        scheduled_meta_data.entry_status = 'NEW'
        scheduled_meta_data.save()
        return scheduled_meta_data

    def query_lab_entry(self, model_name, panel, visit_definition):
        return LabEntry.objects.get(model_name=model_name, requisition_panel=panel, visit_definition=visit_definition)

    

    def create_requisition_meta_data(self, appointment, lab_entry, registered_subject):
        requisition_meta_data = self.query_requisition_meta_data(appointment, lab_entry, registered_subject)
        if not requisition_meta_data:
            requisition_meta_data = RequisitionMetaData.objects.create(appointment=appointment, lab_entry=lab_entry, registered_subject=registered_subject)
        requisition_meta_data.entry_status = 'NEW'
        requisition_meta_data.save()
        return requisition_meta_data

    def remove_all_meta_data(self, appointment, registered_subject, scheduled_meta_data, requisition_meta_data):
        flag = False
        #Ensure there are no keyed forms
        for meta_data in scheduled_meta_data:
            if meta_data.entry_status == 'KEYED':
                flag = True
        #Ensure there are no keyed lab requisitions
        for rmeta_data in requisition_meta_data:
            if rmeta_data.entry_status == 'KEYED':
                flag = True
        if not flag:
            scheduled_meta_data.delete()
            requisition_meta_data.delete()
            return True
        else:
            return False

    def check_instance(self, appointment):
        if appointment.visit_instance != '0':
            appointment = Appointment.objects.get(registered_subject=appointment.registered_subject,
                         visit_instance='0', visit_definition=appointment.visit_definition)
        return appointment
