# import unittest
# import time
#
# from selenium import webdriver
#
# from .microbiome_finders import *
# from microbiome.apps.mb_maternal.tests.functional_tests.microbiome_pages import LoginPage, AdminPage
#
#
# class TestMicrobiomePages(unittest.TestCase):
#
#    def setUp(self):
#        self.driver = webdriver.Firefox()
#        self.driver.get('http://0.0.0.0:8000/admin')
#        time.sleep(1)
#
#    def test_mylogin(self):
#        page = LoginPage(self.driver)
#        login = page.mylogin()
#        self.assertIn('/admin/', login.get_url())
#
#    def test_check_eligibility_link(self):
#        self.test_mylogin()
#        page = AdminPage(self.driver)
#        self.assertTrue('Microbiome Administration', page)
#        self.assertTrue('Maternal Eligibility', page)
#        page.check_eligibility_link()
#        page.click_add_eligibility()
#
#    def test_check_and_click_consent_link(self):
#        self.test_mylogin()
#        page = AdminPage(self.driver)
#        self.assertTrue('Maternal Consent', page)
#        page.check_consent_link()
#        page.click_add_consent()
#
#    def tearDown(self):
#        self.driver.close()
#
# if __name__ == "__main__":
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestMicrobiomePages)
#    unittest.TextTestRunner(verbosity=2).run(suite)
