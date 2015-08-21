from ..tests import BaseSeleniumTest


class LoginSeleniumTest(BaseSeleniumTest):

    def test_success_login(self):
        self.login()
        self.assertEqual(self.browser.current_url, 'http://localhost:8081/home/')

    def test_failed_login(self):
        self.username = 'testuser_y'
        self.password = '12345_y'
        self.login()
        self.assertEqual(self.browser.current_url, 'http://localhost:8081/login/')

    def test_failed_login_with_message(self):
        self.username = 'testuser_y'
        self.password = '12345_y'
        self.login()
        self.assertTrue(self.browser.find_element_by_name('login_message_name').is_displayed())
