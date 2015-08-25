import time

from microbiome.tests.base_selenium_test import BaseSeleniumTest


class TestDashboardSelenium(BaseSeleniumTest):

    def test_left_sidebar_exists(self):
        '''Asserts user can open microbiome home page after login.'''
        self.login()
        time.sleep(1)
        self.browser.get(self.live_server_url + '/dashboard/')
        self.assertIsNotNone(self.browser.find_element_by_id('sidebarLeft').text)

    def test_right_sidebar_exists(self):
        '''Asserts user can open microbiome home page after login.'''
        self.login()
        time.sleep(1)
        self.browser.get(self.live_server_url + '/dashboard/')
        self.assertIsNotNone(self.browser.find_element_by_id('sidebarRight').text)
