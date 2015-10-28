from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .classes import MaternalDashboard

urlpatterns = []

for pattern in MaternalDashboard.get_urlpatterns():
    urlpatterns.append(
        url(pattern,
            login_required(MaternalDashboard.as_view()),
            name=MaternalDashboard.dashboard_url_name))
