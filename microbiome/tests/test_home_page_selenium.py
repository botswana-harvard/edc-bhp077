import time

from selenium.webdriver.common.keys import Keys

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
        infant_link_text = self.browser.find_element_by_id('infant_eligibility')
        if infant_link_text.text == 'Infant':
            infant_link_text.click()

    def test_enrollment_link(self):
        self.login()
        time.sleep(1)
        enrollment_link = self.browser.find_element_by_id('enrollment')
        enrollment_link.click()
        self.browser.save_screenshot('microbiome/screenshots/eligibility_pre.png')

    def test_search_no_search_results(self):
        self.login()
        time.sleep(1)
        self.browser.get(self.live_server_url + '/maternal_search')
        time.sleep(1)
        search_text = self.browser.find_element_by_id('identifier_search')
        search_text.send_keys('test_search')
        search_text.send_keys(Keys.RETURN)
        search_result = self.browser.find_elements_by_id('no_search_results')
        time.sleep(1)
        self.assertTrue(any('No search results for' in item.text for item in search_result))
        self.browser.save_screenshot('microbiome/screenshots/search_result.png')
