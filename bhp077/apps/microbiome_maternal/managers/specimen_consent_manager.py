from django.db import models
from django.db.models import get_model


class SpecimenConsentManager(models.Manager):

    def get_by_natural_key(self, subject_identifier_as_pk):
        RegisteredSubject = get_model('registration', 'RegisteredSubject')
        registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(registered_subject=registered_subject)
