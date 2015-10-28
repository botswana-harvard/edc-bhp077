from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls import include, url, patterns
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.db.models import get_models
from django.views.generic import RedirectView

import django_databrowse

from dajaxice.core import dajaxice_autodiscover, dajaxice_config

from edc.data_manager.classes import data_manager
from edc.dashboard.section.classes import site_sections
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.dashboard.subject.views import additional_requisition
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.subject.visit_schedule.classes import site_visit_schedules

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration

site_lab_profiles.autodiscover()
dajaxice_autodiscover()
MicrobiomeConfiguration().prepare()
site_visit_schedules.autodiscover()
site_visit_schedules.build_all()
site_rule_groups.autodiscover()
site_lab_tracker.autodiscover()
data_manager.prepare()
site_sections.autodiscover()
site_sections.update_section_lists()
admin.autodiscover()
# admin.site.site_header = 'Microbiome Administration'

for model in get_models():
    try:
        django_databrowse.site.register(model)
    except:
        pass

APP_NAME = settings.APP_NAME

urlpatterns = patterns(
    '',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/logout/$', RedirectView.as_view(url='/{app_name}/logout/'.format(app_name=APP_NAME))),
    (r'^admin/', include(admin.site.urls)),
    (r'^i18n/', include('django.conf.urls.i18n')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

urlpatterns += patterns(
    '',
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
)

urlpatterns += patterns(
    '',
    url(r'^databrowse/(.*)', login_required(django_databrowse.site.root)),
)

urlpatterns += patterns(
    '',
    url(r'^/dashboard/'.format(app_name=APP_NAME),
        include('bhp077.apps.{app_name}_dashboard.urls'.format(app_name=APP_NAME))),
)

urlpatterns += patterns(
    '',
    url(r'^{app_name}/login/'.format(app_name=APP_NAME),
        'django.contrib.auth.views.login',
        name='{app_name}_login'.format(app_name=APP_NAME)),
    url(r'^{app_name}/logout/'.format(app_name=APP_NAME),
        'django.contrib.auth.views.logout_then_login',
        name='{app_name}_logout'.format(app_name=APP_NAME)),
    url(r'^{app_name}/password_change/'.format(app_name=APP_NAME),
        'django.contrib.auth.views.password_change',
        name='password_change_url'.format(app_name=APP_NAME)),
    url(r'^{app_name}/password_change_done/'.format(app_name=APP_NAME),
        'django.contrib.auth.views.password_change_done',
        name='password_change_done'.format(app_name=APP_NAME)),
)
urlpatterns += patterns(
    '',
    url(r'^{app_name}/section/'.format(app_name=APP_NAME), include('edc.dashboard.section.urls'), name='section'),
)

urlpatterns += patterns(
    '',
    url(r'^{app_name}/$'.format(app_name=APP_NAME),
        RedirectView.as_view(url='/{app_name}/section/'.format(app_name=APP_NAME))),
    url(r'', RedirectView.as_view(url='/{app_name}/section/'.format(app_name=APP_NAME))),
)

urlpatterns += staticfiles_urlpatterns()
