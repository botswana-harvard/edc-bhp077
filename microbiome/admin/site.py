from django.contrib.admin import AdminSite


class MicrobiomeAdminSite(AdminSite):

    site_header = 'Microbiome administration'
    site_title = 'Microbiome site admin'
    login_template = 'login.html'
    logout_template = 'login.html'
admin_site = MicrobiomeAdminSite(name='microbiomeadmin')
