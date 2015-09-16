from selenium.webdriver.common.by import By


class BasePage(object):
    def __init__(self, browser):
        self.browser = browser


class LoginPage(BasePage):
    username = (By.ID, 'username')
    password = (By.ID, 'password')
    login_button = (By.ID, 'login')
    login_error = (By.ID, 'login_message')

    def set_username(self, username):
        usernameElement = self.browser.find_element(*LoginPage.username)
        usernameElement.send_keys(username)

    def set_password(self, password):
        passwordElement = self.browser.find_element(*LoginPage.password)
        passwordElement.send_keys(password)

    def click_login(self):
        self.browser.find_element(*LoginPage.login_button).click()

    def authentication_failed(self):
        notifcationElement = self.browser.find_element(*LoginPage.login_error)
        return notifcationElement.is_displayed()

    def login(self, username, password):
        self.set_username(username)
        self.set_password(password)
        self.click_login()
