from edc.dashboard.search.classes import BaseSearchByWord
from ..models import InfantBirth


class InfantSearchByWord(BaseSearchByWord):

    name = 'word'
    search_model = InfantBirth
    order_by = '-created'
    template = 'infantbirth_include.html'
