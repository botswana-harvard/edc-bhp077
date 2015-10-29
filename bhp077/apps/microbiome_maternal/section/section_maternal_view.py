from edc.dashboard.section.classes import BaseSectionView, site_sections

from ..search import MaternalSearchByWord
from ..models import MaternalEligibility


class SectionMaternalView(BaseSectionView):
    section_name = 'maternal'
    section_display_name = 'Mothers'
    section_display_index = 10
    section_template = 'section_maternal.html'
    dashboard_url_name = 'subject_dashboard_url'
    add_model = MaternalEligibility
    search = {'word': MaternalSearchByWord}
    show_most_recent = True

#     def contribute_to_context(self, context, request, *args, **kwargs):
#         current_survey = None
#         if settings.CURRENT_SURVEY:
#             current_survey = Survey.objects.current_survey()
#         context.update({
#             'current_survey': current_survey,
#             'current_community': str(site_mappers.get_current_mapper()),
#             'mapper_name': site_mappers.get_current_mapper().map_area,
#             'gps_search_form': GpsSearchForm(initial={'radius': 100}),
#             'use_gps_to_target_verification': settings.VERIFY_GPS,
#             'search_term': kwargs.get('search_term'),
#         })
#         context.update()
#         return context

site_sections.register(SectionMaternalView)
