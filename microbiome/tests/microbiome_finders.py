from selenium.webdriver.common.by import By

'''Define web objects for Microbiome main pages'''


class LoginFinder(object):
    TITLE = (By.CLASS_NAME, "login")
    USERNAME = (By.NAME, 'username')
    PASSWORD = (By.NAME, 'password')
    SUBMIT = (By.CSS_SELECTOR, "input[type='submit']")


class AdminFinder(object):
    TITLE = (By.CSS_SELECTOR, 'h1')
    ELIGIBILITY_LINK = (By.LINK_TEXT, 'Maternal Eligibility')
    ADD_ELIGIBILITY_LINK = (By.LINK_TEXT, 'Add Maternal Eligibility')
