from django.core.exceptions import MultipleObjectsReturned

from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData

from edc.subject.entry.models import Entry, LabEntry
from edc.subject.appointment.models import Appointment

from edc_constants.constants import NEW, KEYED


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

    def entry_model_options(self, app_label, model_name):
        model_options = {}
        model_options.update(
            entry__app_label=app_label,
            entry__model_name=model_name,
            appointment=self.appointment)
        return model_options

    def lab_entry_model_options(self, app_label, model_name, panel_name):
        model_options = {}
        model_options.update(
            lab_entry__app_label=app_label,
            lab_entry__model_name=model_name,
            appointment=self.appointment,
            lab_entry__requisition_panel__name=panel_name)
        return model_options

    def update_requistion_entry_meta_data(self, app_label, model_name, panel_name):
        try:
            rq = RequisitionMetaData.objects.get(
                **self.lab_entry_model_options(app_label, model_name, panel_name))
            rq.entry_status = NEW
            rq.save()
        except RequisitionMetaData.DoesNotExist:
            pass
        except AttributeError:
            pass

    def update_scheduled_entry_meta_data(self, app_label, model_name):
        try:
            sd = ScheduledEntryMetaData.objects.get(**self.entry_model_options(app_label, model_name))
            sd.entry_status = NEW
            sd.save()
        except ScheduledEntryMetaData.DoesNotExist:
            pass
        except AttributeError:
            pass

    def query_entry(self, model_name, visit_definition):
        try:
            return Entry.objects.get(model_name=model_name, visit_definition=visit_definition)
        except Entry.DoesNotExist:
            return False

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
            scheduled_meta_data = ScheduledEntryMetaData.objects.create(
                appointment=appointment, entry=entry, registered_subject=registered_subject
            )
        scheduled_meta_data.entry_status = NEW
        scheduled_meta_data.save()
        return scheduled_meta_data

    def lab_entry(self, model_name, panel, visit_definition):
        return LabEntry.objects.get(model_name=model_name, requisition_panel=panel, visit_definition=visit_definition)

    def requisition_meta_data(self, appointment, lab_entry, registered_subject):
        requisition_meta_data = RequisitionMetaData.objects.filter(
            appointment=appointment, lab_entry=lab_entry, registered_subject=registered_subject
        )
        if requisition_meta_data.count() == 1:
            return requisition_meta_data[0]
        return requisition_meta_data

    def create_requisition_meta_data(self, appointment, lab_entry, registered_subject):
        requisition_meta_data = self.query_requisition_meta_data(appointment, lab_entry, registered_subject)
        if not requisition_meta_data:
            requisition_meta_data = RequisitionMetaData.objects.create(appointment=appointment, lab_entry=lab_entry, registered_subject=registered_subject)
        requisition_meta_data.entry_status = NEW
        requisition_meta_data.save()
        return requisition_meta_data

    def remove_all_meta_data(self, appointment, registered_subject, scheduled_meta_data, requisition_meta_data):
        flag = False
        #Ensure there are no keyed forms
        for meta_data in scheduled_meta_data:
            if meta_data.entry_status == KEYED:
                flag = True
        #Ensure there are no keyed lab requisitions
        for rmeta_data in requisition_meta_data:
            if rmeta_data.entry_status == KEYED:
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
