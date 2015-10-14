from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .classes import MaternalDashboard

# regex = {}
# regex['dashboard_type'] = 'maternal'
# regex['dashboard_model'] = 'maternal_consent'
# urlpatterns += MaternalDashboard.get_urlpatterns('microbiome.dashboard.views',
#                                                  regex, visit_field_names=['maternal_visit', ])

urlpatterns = []

for pattern in MaternalDashboard.get_urlpatterns():
    urlpatterns.append(
        url(pattern,
            login_required(MaternalDashboard.as_view()),
            name=MaternalDashboard.dashboard_url_name))
