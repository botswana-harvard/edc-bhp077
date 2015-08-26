from microbiome.tests.base_selenium_test import BaseSeleniumTest


class TestMicrobiomeHomePageSelenium(BaseSeleniumTest):

    def test_open_microbiome_home_page(self):
        '''Asserts user can open microbiome home page after login.'''
        self.login()
        self.assertTrue('Microbiome', self.browser.title)
        self.browser.save_screenshot('microbiome/screenshots/home_page.png')

    def test_maternal_toolbar_links(self):
        '''Assert maternal link.'''
        self.login()
        maternal_link_text = self.browser.find_element_by_link_text('MATERNAL').text
        self.assertEqual('MATERNAL', maternal_link_text)

    def test_infant_toolbar_links(self):
        '''Assert infant link test.'''
        self.login()
        martenal_link_text = self.browser.find_element_by_link_text('INFANT').text
        self.assertEqual('INFANT', martenal_link_text)

    def test_enrollment_link(self):
        self.login()
        enrollment_link = self.browser.find_element_by_id('enrollment')
        enrollment_link.click()
        self.browser.save_screenshot('microbiome/screenshots/eligibility_pre.png')
