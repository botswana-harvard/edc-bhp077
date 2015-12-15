from django.db import models


class ScheduledModelManager(models.Manager):
    """Manager for all scheduled models (those with a infant_visit fk)."""
    def get_by_natural_key(self, visit_instance, code, subject_identifier_as_pk):
        Appointment = models.get_model('appointment', 'appointment')
        appointment = Appointment.objects.get_by_natural_key(visit_instance, code, subject_identifier_as_pk)
        return self.get(appointment=appointment)

