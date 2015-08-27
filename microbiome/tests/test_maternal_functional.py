import time
from microbiome.tests.base_selenium_test import BaseSeleniumTest


class TestMaternalFunctional(BaseSeleniumTest):

    def test_maternal_screening(self):
        '''Go to screening page and take screen shot'''
        self.login()
        self.browser.find_element_by_xpath('//*[@id="enrollment"]').click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Microbiome administration', body.text)
        self.browser.save_screenshot('microbiome/screenshots/maternal_screening.png')

    def test_microbiome_link(self):
        '''Click on microbiome link'''
        self.login()
        self.browser.find_element_by_xpath('//*[@id="enrollment"]').click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Microbiome administration', body.text)
        self.browser.find_element_by_link_text('Microbiome').click()
        time.sleep(1)

    def test_maternal_consent(self):
        '''Navigate to Consent and take screen shot'''
        self.login()
        self.browser.find_element_by_xpath('//*[@id="enrollment"]').click()
        # self.browser.find_element_by_xpath("//img[contains(@src, 'home_page_button.png')]").click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Microbiome administration', body.text)
        self.browser.find_element_by_link_text('Microbiome').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Subject consents').click()
        self.browser.find_element_by_link_text('Add subject consent').click()
        self.browser.save_screenshot('microbiome/screenshots/maternal_consent.png')
        time.sleep(1)

    def test_maternal_locator(self):
        '''Navigate to Locator and take screen shot'''
        self.login()
        self.browser.find_element_by_xpath('//*[@id="enrollment"]').click()
        # self.browser.find_element_by_xpath("//img[contains(@src, 'home_page_button.png')]").click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Microbiome administration', body.text)
        self.browser.find_element_by_link_text('Microbiome').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Maternal Locator').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Add Maternal Locator').click()
        self.browser.save_screenshot('microbiome/screenshots/maternal_locator.png')

    def test_maternal_infected(self):
        '''Navigate to Infected and take screen shot'''
        self.login()
        # self.browser.find_element_by_xpath("//img[contains(@src, 'home_page_button.png')]").click()
        self.browser.find_element_by_xpath('//*[@id="enrollment"]').click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Microbiome administration', body.text)
        self.browser.find_element_by_link_text('Microbiome').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Maternal Infected').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Add Maternal Infected').click()
        self.browser.save_screenshot('microbiome/screenshots/maternal_infected.png')

    def test_maternal_labour_delivery(self):
        '''Navigate to Labour and delivery and take screen shot'''
        self.login()
        self.browser.find_element_by_xpath('//*[@id="enrollment"]').click()
        # self.browser.find_element_by_xpath("//img[contains(@src, 'home_page_button.png')]").click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Microbiome administration', body.text)
        self.browser.find_element_by_link_text('Microbiome').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Maternal Labour & Deliverys').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Add Maternal Labour & Delivery').click()
        self.browser.save_screenshot('microbiome/screenshots/maternal_labour_delivery.png')

    def test_maternal_arv_preg(self):
        '''Navigate to Arv Preg and take screen shot'''
        self.login()
        self.browser.find_element_by_xpath('//*[@id="enrollment"]').click()
        # self.browser.find_element_by_xpath("//img[contains(@src, 'home_page_button.png')]").click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Microbiome administration', body.text)
        self.browser.find_element_by_link_text('Microbiome').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Maternal arv pregs').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Add maternal arv preg').click()
        self.browser.save_screenshot('microbiome/screenshots/maternal_arv_preg.png')

    def test_maternal_labdel_preg_dx(self):
        '''Navigate to Maternal Labour and Delivery Preg Dx and take screen shot'''
        self.login()
        self.browser.find_element_by_xpath('//*[@id="enrollment"]').click()
        # self.browser.find_element_by_xpath("//img[contains(@src, 'home_page_button.png')]").click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Microbiome administration', body.text)
        self.browser.find_element_by_link_text('Microbiome').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Maternal Labour & Delivery: Preg Dxs').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Add Maternal Labour & Delivery: Preg Dx').click()
        self.browser.save_screenshot('microbiome/screenshots/maternal_lab_del_preg_dx.png')

    def test_maternal_labdel_preg_dxt(self):
        '''Navigate to Maternal Labour and Delivery Preg DxT and take screen shot'''
        self.login()
        self.browser.find_element_by_xpath('//*[@id="enrollment"]').click()
        # self.browser.find_element_by_xpath("//img[contains(@src, 'home_page_button.png')]").click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Microbiome administration', body.text)
        self.browser.find_element_by_link_text('Microbiome').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Maternal Labour & Delivery: Preg DxTs').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Add Maternal Labour & Delivery: Preg DxT').click()
        self.browser.save_screenshot('microbiome/screenshots/maternal_lab_del_preg_dxT.png')

    def test_maternal_labdel_med_history(self):
        '''Navigate to Maternal Labour and Delivery Med History and take screen shot'''
        self.login()
        self.browser.find_element_by_xpath('//*[@id="enrollment"]').click()
        # self.browser.find_element_by_xpath("//img[contains(@src, 'home_page_button.png')]").click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Microbiome administration', body.text)
        self.browser.find_element_by_link_text('Microbiome').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Maternal Labour & Delivery: MedHistorys').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Add Maternal Labour & Delivery: MedHistory').click()
        self.browser.save_screenshot('microbiome/screenshots/maternal_lab_del_med_history.png')

    def test_maternal_labdel_clinic_history(self):
        '''Navigate to Maternal Labour and Delivery Clinic History and take screen shot'''
        self.login()
        self.browser.find_element_by_xpath('//*[@id="enrollment"]').click()
        # self.browser.find_element_by_xpath("//img[contains(@src, 'home_page_button.png')]").click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Microbiome administration', body.text)
        self.browser.find_element_by_link_text('Microbiome').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Maternal Labour & Delivery: ClinHists').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Add Maternal Labour & Delivery: ClinHist').click()
        self.browser.save_screenshot('microbiome/screenshots/maternal_lab_del_clinic_history.png')

    def test_maternal_arv(self):
        '''Navigate to Maternal Arv and take screen shot'''
        self.login()
        self.browser.find_element_by_xpath('//*[@id="enrollment"]').click()
        # self.browser.find_element_by_xpath("//img[contains(@src, 'home_page_button.png')]").click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Microbiome administration', body.text)
        self.browser.find_element_by_link_text('Microbiome').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Maternal ARV').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Add Maternal ARV').click()
        self.browser.save_screenshot('microbiome/screenshots/maternal_arv.png')

    def test_maternal_arv_inpreg_post(self):
        '''Navigate to Maternal Arv Preg Post and take screen shot'''
        self.login()
        self.browser.find_element_by_xpath('//*[@id="enrollment"]').click()
        # self.browser.find_element_by_xpath("//img[contains(@src, 'home_page_button.png')]").click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Microbiome administration', body.text)
        self.browser.find_element_by_link_text('Microbiome').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Maternal ARV In This Preg: PostParts').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Add Maternal ARV In This Preg: PostPart').click()
        self.browser.save_screenshot('microbiome/screenshots/maternal_arv_inpreg_post.png')

    def test_maternal_arv_inpreg_pregnancies(self):
        '''Navigate to Maternal Arv Preg Pregnancies and take screen shot'''
        self.login()
        self.browser.find_element_by_xpath('//*[@id="enrollment"]').click()
        # self.browser.find_element_by_xpath("//img[contains(@src, 'home_page_button.png')]").click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Microbiome administration', body.text)
        self.browser.find_element_by_link_text('Microbiome').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Maternal ARV In This Preg: Pregnancys').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Add Maternal ARV In This Preg: Pregnancy').click()
        self.browser.save_screenshot('microbiome/screenshots/maternal_arv_inpreg_pregnancies.png')

    def test_maternal_post_eligibility(self):
        '''Navigate to Maternal Arv Preg Pregnancies and take screen shot'''
        self.login()
        self.browser.find_element_by_xpath('//*[@id="enrollment"]').click()
        # self.browser.find_element_by_xpath("//img[contains(@src, 'home_page_button.png')]").click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Microbiome administration', body.text)
        self.browser.find_element_by_link_text('Microbiome').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Maternal Eligibility Post').click()
        time.sleep(1)
        self.browser.find_element_by_link_text('Add Maternal Eligibility Post').click()
        self.browser.save_screenshot('microbiome/screenshots/maternal_post_eligibility.png')
