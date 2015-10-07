from datetime import date, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from microbiome_base_page import MicrobiomeBasePage
from maternal_finders import MaternalEligibilityFinder, ConsentFinder
from microbiome_pages import AdminPage
from selenium.webdriver.support.ui import WebDriverWait


'''Defining functions for each maternal page (class)'''


class EligibilityPage(MicrobiomeBasePage):

    def confirm_eligibility_page(self):
        return True if self.find_element(*MaternalEligibilityFinder.HEADING) else False

    def enter_report_date(self):
        self.find_element(*MaternalEligibilityFinder.DATE).send_keys('2015-09-17')

    def enter_report_time(self):
        self.find_element(*MaternalEligibilityFinder.TIME).send_keys('07:50:48')

    def enter_age(self):
        self.find_element(*MaternalEligibilityFinder.PARTICIPANT_AGE).send_keys('18')

    def affirm_pregnancy(self):
        self.find_element(*MaternalEligibilityFinder.PREGNANCY).click()

    def click_save_button(self):
        self.driver.find_element(*MaternalEligibilityFinder.SUBMIT).click()

    def fill_eligibility_form(self):
        self.enter_report_date()
        self.enter_report_time()
        self.enter_age()
        self.affirm_pregnancy()
        # self.click_save_button()
        # return AdminPage(self.driver)


class ConsentPage(MicrobiomeBasePage):

    def enter_first_name(self):
        self.find_element(*ConsentFinder.FIRST_NAME).send_keys('Silver')

    def enter_last_name(self):
        self.find_element(*ConsentFinder.LAST_NAME).send_keys('Apple')

    def enter_initials(self):
        self.find_element(*ConsentFinder.INITIALS).send_keys('SA')

    def click_language(self):
        self.find_element(*ConsentFinder.LANGUAGE).click()

    def click_literacy(self):
        self.find_element(*ConsentFinder.LITERACY).click()

    def enter_consent_date(self):
        self.find_element(*ConsentFinder.CONSENT_DATE).click()

    def enter_consent_time(self):
        self.find_element(*ConsentFinder.CONSENT_TIME).click()

    def click_gender(self):
        self.find_element(*ConsentFinder.GENDER).click()

    def enter_dob(self):
        self.find_element(*ConsentFinder.DOB).send_keys('1997-09-18')

    def click_dob_est(self):
        self.find_element(*ConsentFinder.DOB_EST).click()

    def click_citizenship(self):
        self.find_element(*ConsentFinder.CITIZEN).click()

    def enter_omang(self):
        self.find_element(*ConsentFinder.OMANG_ID).send_keys('111121111')

    def click_id_type(self):
        self.find_element(*ConsentFinder.ID_TYPE).click()

    def enter_confirm_omang(self):
        self.find_element(*ConsentFinder.CONFIRM_OMANG_ID).send_keys('111121111')

    # def click_sample_storage(self):
        # self.find_element(*ConsentFinder.SAMPLE_STORAGE).click()

    def click_to_save_consent(self):
        self.find_element(*ConsentFinder.SUBMIT).click()

    def fill_consent_form(self):
        self.enter_first_name()
        self.enter_last_name()
        self.enter_initials()
        self.click_language()
        self.click_literacy()
        self.enter_consent_date()
        self.enter_consent_time()
        self.click_gender()
        self.enter_dob()
        self.click_dob_est()
        self.click_citizenship()
        self.enter_omang()
        self.click_id_type()
        self.enter_confirm_omang()
        # self.click_sample_storage()
