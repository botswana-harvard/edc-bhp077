import unittest
from maternal_finders import *
from maternal_pages import *
from microbiome_pages import *
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestMaternalPages(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get('http://0.0.0.0:8000/admin')

    def test_eligibility_page(self):
        page = LoginPage(self.driver)
        login = page.mylogin()
        self.assertIn('/admin/', login.get_url())
        page = AdminPage(self.driver)
        page.check_eligibility_link()
        page.click_add_eligibility()
        page = EligibilityPage(self.driver)
        self.assertTrue(page.confirm_eligibility_page())
        page.fill_eligibility_form()
        self.assertTrue('18', page)
        page.click_save_button()

    def tearDown(self):
        self.driver.close()

# gather all tests in a test suite
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMaternalPages)
    unittest.TextTestRunner(verbosity=2).run(suite)
