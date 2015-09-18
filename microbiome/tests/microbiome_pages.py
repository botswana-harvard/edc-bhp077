from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from microbiome_finders import LoginFinder, AdminFinder
from microbiome_base_page import MicrobiomeBasePage


class LoginPage(MicrobiomeBasePage):

    def login_page_title(self):
        self.driver.find_element(*LoginFinder.TITLE)

    def enter_username(self):
        self.driver.find_element(*LoginFinder.USERNAME).send_keys('django')

    def enter_password(self):
        self.driver.find_element(*LoginFinder.PASSWORD).send_keys('12345')

    def click_login_button(self):
        self.driver.find_element(*LoginFinder.SUBMIT).click()

    def mylogin(self):
        self.enter_username()
        self.enter_password()
        self.click_login_button()
        return AdminPage(self.driver)


class AdminPage(MicrobiomeBasePage):

    def admin_page_title(self):
        self.driver.find_element(*AdminFinder.TITLE)

    def check_eligibility_link(self):
        self.driver.find_element(*AdminFinder.ELIGIBILITY_LINK).click()

    def click_add_eligibility(self):
        self.driver.find_element(*AdminFinder.ADD_ELIGIBILITY_LINK).click()
