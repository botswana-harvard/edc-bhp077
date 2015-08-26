import time
from microbiome.tests.base_selenium_test import BaseSeleniumTest


class TestMaternalFunctional(BaseSeleniumTest):

    def test_enroll_mother_button(self):
        '''Login and click enroll mother button'''
        self.login()
        enroll_mother = self.browser.find_elements_by_css_selector("a[href*='/admin/microbiome/maternaleligibilitypre/add/?next=/dashboard/']")
        for mother_link in range(0, len(enroll_mother)):
            mother_link = self.browser.find_elements_by_css_selector("a[href*='/admin/microbiome/maternaleligibilitypre/add/?next=/dashboard/']")
            mother_link[0].click()

    def test_microbiome_link(self):
        '''Confirm page heading and click microbiome link'''
        self.login()
        time.sleep(1)
        enroll_mother = self.browser.find_elements_by_css_selector("a[href*='/admin/microbiome/maternaleligibilitypre/add/?next=/dashboard/']")
        for mylink in range(0, len(enroll_mother)):
            mylink = self.browser.find_elements_by_css_selector("a[href*='/admin/microbiome/maternaleligibilitypre/add/?next=/dashboard/']")
            mylink[0].click()
        time.sleep(1)
        heading = self.browser.title.lower().startswith('Microbiome administration')
        self.assertTrue('Microbiome administration', heading)
        time.sleep(1)
        self.browser.find_element_by_css_selector("a[href*='/admin/microbiome/']").click()
