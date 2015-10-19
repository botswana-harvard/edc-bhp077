from django.core.urlresolvers import reverse

from .base_mother import BaseMother


class MaternalUninfected(BaseMother):

    def get_absolute_url(self):
        return reverse('admin:microbiome_maternaluninfected_change', args=(self.id,))

    class Meta:
        app_label = 'microbiome'
        verbose_name = 'Maternal Uninfected'
        verbose_name_plural = 'Maternal Uninfected'
