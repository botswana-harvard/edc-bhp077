from django.core.urlresolvers import reverse
from django.db import models

from edc.subject.registration.models import RegisteredSubject
# from edc_base.model.models import BaseUuidModel

from lis.specimen.lab_receive.models import BaseReceive


class Receive(BaseReceive):

    registered_subject = models.ForeignKey(RegisteredSubject, null=True, related_name='microbiome_receive')

    requisition_model_name = models.CharField(max_length=25, null=True, editable=False)

    subject_type = models.CharField(max_length=25, null=True, editable=False)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.subject_type = self.registered_subject.subject_type
        super(Receive, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.receive_identifier or u''

    def deserialize_get_missing_fk(self, attrname):
        retval = None
        return retval

    def requisition(self):
        url = reverse('admin:microbiome_lab_maternalrequisition_changelist')
        return '<a href="{0}?q={1}">{1}</a>'.format(url, self.requisition_identifier)
    requisition.allow_tags = True

    def natural_key(self):
        return (self.receive_identifier, )

    class Meta:
        app_label = 'microbiome_lab'
