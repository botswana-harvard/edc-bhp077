from django.core.urlresolvers import reverse

from .base_mother import BaseMother


class MaternalUninfected(BaseMother):

    def get_absolute_url(self):
        return reverse('admin:microbiome_maternal_maternaluninfected_change', args=(self.id,))

    class Meta:
        app_label = 'microbiome_maternal'
        verbose_name = 'Maternal Uninfected'
        verbose_name_plural = 'Maternal Uninfected'
