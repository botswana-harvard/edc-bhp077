from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from microbiome_base_page import MicrobiomeBasePage
from maternal_finders import MaternalEligibilityFinder
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
    pass
