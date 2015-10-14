from edc.dashboard.search.classes import BaseSearchByWord
from ..models import MaternalEligibility


class MaternalSearchByWord(BaseSearchByWord):

    name = 'word'
    search_model = MaternalEligibility
    order_by = ['-created']
    template = 'maternaleligibility_include.html'
