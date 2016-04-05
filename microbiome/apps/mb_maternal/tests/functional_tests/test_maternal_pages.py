# import unittest
#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# from .maternal_finders import *
# from .microbiome_finders import *
# from microbiome.apps.mb_maternal.tests.functional_tests.maternal_pages import EligibilityPage, ConsentPage
# from microbiome.apps.mb_maternal.tests.functional_tests.microbiome_pages import LoginPage, AdminPage
#
#
# class TestMaternalPages(unittest.TestCase):
#
#    def setUp(self):
#        self.driver = webdriver.Firefox()
#        self.driver.get('http://0.0.0.0:8000/admin')
#
#    def test_eligibility_page(self):
#        page = LoginPage(self.driver)
#        login = page.mylogin()
#        self.assertIn('/admin/', login.get_url())
#        page = AdminPage(self.driver)
#        page.check_eligibility_link()
#        page.click_add_eligibility()
#        page = EligibilityPage(self.driver)
#        self.assertTrue(page.confirm_eligibility_page())
#        page.fill_eligibility_form()
#        self.assertTrue('18', page)
#        page.click_save_button()
#
#    def test_find_consent_link_and_fill(self):
#        page = LoginPage(self.driver)
#        login = page.mylogin()
#        self.assertIn('/admin/', login.get_url())
#        page = AdminPage(self.driver)
#        self.assertTrue('Maternal Consent', page)
#        page.check_consent_link()
#        page.click_add_consent()
#        self.assertTrue('Add Maternal Consent', page)
#        page = ConsentPage(self.driver)
#        page.fill_consent_form()
#        page.click_to_save_consent()
#
#    def tearDown(self):
#        self.driver.close()
#
# # gather all tests in a test suite
# if __name__ == "__main__":
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestMaternalPages)
#    unittest.TextTestRunner(verbosity=2).run(suite)
