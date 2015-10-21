from edc.dashboard.section.classes import BaseSectionView, site_sections

from .maternal_search_by_word import MaternalSearchByWord
from .models import MaternalEligibility


class SectionMaternalView(BaseSectionView):
    section_name = 'maternal'
    section_display_name = 'Mothers'
    section_display_index = 10
    section_template = 'section_maternal.html'
    dashboard_url_name = 'subject_dashboard_url'
    add_model = MaternalEligibility
    search = {'word': MaternalSearchByWord}
    show_most_recent = True

site_sections.register(SectionMaternalView)
