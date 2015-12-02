from django.db import models


class AntenatalEnrollmentManager(models.Manager):

    def get_queryset(self):
        return super(AntenatalEnrollmentManager, self).get_queryset().filter(
            enrollment_type='antenatal')

    def create(self, **kwargs):
        kwargs.update({'enrollment_type': 'antenatal'})
        return super(AntenatalEnrollmentManager, self).create(**kwargs)
