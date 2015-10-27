from edc.dashboard.section.classes import BaseSectionForDashboardView, site_sections


class SectionInfantView(BaseSectionForDashboardView):
    section_name = 'infant'
    section_display_name = 'Infants'
    section_display_index = 30
    section_template = 'section_infant.html'
    dashboard_url_name = 'subject_dashboard_url'
site_sections.register(SectionInfantView)
