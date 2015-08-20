from ..tests import BaseSeleniumTest


class LoginSeleniumTest(BaseSeleniumTest):

    def test_success_login(self):
        self.login()
        self.assertEqual(self.browser.current_url, 'http://localhost:8000/home/')

    def test_failed_login(self):
        self.login()
        login_message = self.browser.find_element_by_name('login_message_name')
        self.assertIn('Wrong', login_message)
