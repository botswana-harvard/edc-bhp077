import time

from selenium import webdriver
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .pages import LoginPage


class LoginSeleniumTest(StaticLiveServerTestCase):
    username = 'testuser'
    password = '12345'
    email = 'testuser@123.org'

    def setUp(self):
        User.objects.create_superuser(self.username, self.email, self.password)
        super().setUp()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

    def tearDown(self):
        self.browser.quit()

    def test_success_login(self):
        self.login_page = LoginPage(self.browser)
        self.login_page.login(self.username, self.password)
        time.sleep(1)
        self.assertIn('/home/', self.browser.current_url)

    def test_login_incorect_username(self):
        self.login_page = LoginPage(self.browser)
        self.login_page.login('test', self.password)
        time.sleep(2)
        self.assert_(self.login_page.authentication_failed())

    def test_login_incorect_password(self):
        self.login_page = LoginPage(self.browser)
        self.login_page.login(self.username, 'test')
        time.sleep(2)
        self.assert_(self.login_page.authentication_failed())
