import time

from .base_selenium_test import BaseSeleniumTest


class TestDashboardSelenium(BaseSeleniumTest):

    def test_right_sidebar_exists(self):
        """Assert that right side bar exists on dashboard"""
        self.login()
        time.sleep(1)
        self.browser.get(self.live_server_url + '/dashboard/')
        self.assertIsNotNone(self.browser.find_element_by_id('sidebarRight').text)
