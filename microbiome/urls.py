"""xx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url
from django.contrib import admin

from microbiome.views import (
    HomeView, SubjectDashboardView, login_view, logout_view, MaternalSearchView
)


admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/', login_view),
    url(r'^login/', login_view, name='login_url'),
    url(r'^logout/', logout_view, name='logout_url'),
    url(r'^home/', HomeView.as_view(), name='home'),
    url(r'^dashboard/', SubjectDashboardView.as_view(), name='dashboard'),
    url(r'maternal_search/', MaternalSearchView.as_view(), name='maternal_search'),
    url(r'^$', HomeView.as_view(), name='default'),
]
