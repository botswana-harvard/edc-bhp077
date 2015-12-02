from dateutil import rrule

from bhp077.apps.microbiome.base_model_form import BaseModelForm

from ..models import MaternalVisit


class BaseMaternalModelForm(BaseModelForm):

    visit_model = MaternalVisit

    def weeks_between(self, start_date, end_date):
        weeks = rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)
        return weeks.count()
