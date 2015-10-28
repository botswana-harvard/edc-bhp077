from django.db import models


class ScheduledModelManager(models.Manager):
    """Manager for all scheduled models (those with a subject_visit fk)."""
    def get_by_natural_key(self, report_datetime, visit_instance, code, subject_identifier_as_pk):
        MaternalVisit = models.get_model('microbiome', 'MaternalVisit')
        maternal_visit = MaternalVisit.objects.get_by_natural_key(report_datetime,
                                                                  visit_instance,
                                                                  code,
                                                                  subject_identifier_as_pk)
        return self.get(subject_visit=maternal_visit)
