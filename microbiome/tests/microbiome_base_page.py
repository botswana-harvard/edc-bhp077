import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class MicrobiomeBasePage(object):

    '''This is the base page that carries attributes for every microbiome page'''

    # setting the main page url
    def __init__(self, driver, base_url='http://0.0.0.0:8000'):
        self.base_url = base_url
        self.driver = driver
        self.timeout = 30
        time.sleep(1)

    # find elements based on what is defined
    def find_element(self, *microbiome_finders):
        return self.driver.find_element(*microbiome_finders)

    # indicate what url to open
    def open(self, url):
        url = self.base_url + '/admin/'
        self.driver.get(url)

    # confirms title on a page
    def get_title(self):
        return self.driver.title

    # get url of the current loaded page
    def get_url(self):
        return self.driver.current_url

    # getting ready to click on something
    def mouse_over(self, *microbiome_finders):
        my_element = self.find_element(*microbiome_finders)
        mouse_over = ActionChains(self.driver).move_to_element(my_element)
        mouse_over.perform()
