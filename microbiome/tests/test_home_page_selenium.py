from microbiome.tests.base_selenium_test import BaseSeleniumTest


class TestReceiveSelenium(BaseSeleniumTest):

    def test_open_microbiome_home_page(self):
        '''Asserts user can open microbiome home page'''
        self.login()
        self.assertTrue('Microbiome', self.browser.title)
        self.browser.save_screenshot('microbiome/screenshots/home_page.png')
