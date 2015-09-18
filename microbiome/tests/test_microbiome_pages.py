import unittest
import time
from microbiome_finders import *
from microbiome_pages import LoginPage, AdminPage
from selenium import webdriver


class TestMicrobiomePages(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get('http://0.0.0.0:8000/admin')
        time.sleep(1)

    def test_mylogin(self):
        page = LoginPage(self.driver)
        login = page.mylogin()
        self.assertIn('/admin/', login.get_url())

    def test_check_eligibility_link(self):
        self.test_mylogin()
        page = AdminPage(self.driver)
        self.assertTrue('Microbiome Administration', page)
        page.check_eligibility_link()
        page.click_add_eligibility()

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMicrobiomePages)
    unittest.TextTestRunner(verbosity=2).run(suite)
