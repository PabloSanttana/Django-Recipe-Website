# sobe o servidor completo
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By

from utils.browser import make_chrome_browser
import time


class AuthorBaseFunctionTestCase(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, s=3):
        time.sleep(s)

    def create_user_defualt_is_valid(self):
        self.browser.get(self.live_server_url + '/authors/register')
        form = self.get_form()
        self.get_by_name(form, "first_name").send_keys("Rafaela")
        self.get_by_name(form, "last_name").send_keys("Santana")
        self.get_by_name(form, "username").send_keys("rafaelaSantana")
        self.get_by_name(form, "email").send_keys("rafaela@gmail.com")
        self.get_by_name(form, "password").send_keys("Ab123456789")
        self.get_by_name(form, "password2").send_keys("Ab123456789")
        form.submit()

    def get_by_name(self, form, name):
        return form.find_element(By.NAME, name)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH, "/html/body/main/div[2]/form")
