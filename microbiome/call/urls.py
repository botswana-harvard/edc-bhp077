from django.conf.urls import url
from .views import GenerateCallList

urlpatterns = [
    url(r'^about/', GenerateCallList.as_view(template_name="about.html")),
]
