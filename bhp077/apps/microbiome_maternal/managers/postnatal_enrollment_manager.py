from django.db import models


class PostnatalEnrollmentManager(models.Manager):

    def get_queryset(self):
        return super(PostnatalEnrollmentManager, self).get_queryset().filter(
            enrollment_type='postnatal')

    def create(self, **kwargs):
        kwargs.update({'enrollment_type': 'postnatal'})
        return super(PostnatalEnrollmentManager, self).create(**kwargs)
