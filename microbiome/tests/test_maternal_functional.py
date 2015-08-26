from microbiome.tests.base_selenium_test import BaseSeleniumTest


class TestMaternalFunctional(BaseSeleniumTest):

    def test_enroll_mother_button(self):
        '''Login and click enroll mother button'''
        self.login()
        enroll_mother = self.browser.find_elements_by_css_selector("a[href*='/admin/microbiome/maternaleligibilitypre/add/?next=/dashboard/']")
        for e in range(0, len(enroll_mother)):
            mylink = self.browser.find_elements_by_css_selector("a[href*='/admin/microbiome/maternaleligibilitypre/add/?next=/dashboard/']")
            mylink[0].click()
