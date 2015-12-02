from django.conf.urls import url
from .views import GenerateCallList

urlpatterns = [
    url(r'^antenatal_call_list/', GenerateCallList.as_view(), name='antenatal_call_list_url'),
]
