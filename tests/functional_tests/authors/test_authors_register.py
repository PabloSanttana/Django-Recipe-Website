from .base import AuthorBaseFunctionTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized


class AuthorsRegisterFunctionTestCase(AuthorBaseFunctionTestCase):
    def get_by_name(self, form, name):
        return form.find_element(By.NAME, name)

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, "input")

        for field in fields:
            if field.is_displayed():
                field.send_keys(" " * 20)
        form.find_element(By.NAME, "email").send_keys("email@example")

    def get_form(self):
        return self.browser.find_element(
            By.XPATH, "/html/body/main/div[2]/form")

    def form_user_registers(self, form):
        self.get_by_name(form, "first_name").send_keys("Rafaela")
        self.get_by_name(form, "last_name").send_keys("Santana")
        self.get_by_name(form, "username").send_keys("rafaelaSantana")
        self.get_by_name(form, "email").send_keys("rafaela@gmail.com")
        self.get_by_name(form, "password").send_keys("Ab123456789")
        self.get_by_name(form, "password2").send_keys("Ab123456789")
        self.get_by_name(form, "first_name").send_keys(Keys.ENTER)

    def form_user_login(self, form):
        self.get_by_name(form, "username").send_keys("rafaelaSantana")
        self.get_by_name(form, "password").send_keys("Ab123456789")
        self.get_by_name(form, "password").send_keys(Keys.ENTER)

    @parameterized.expand([
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('username', 'This field is required'),
        ('password', 'Password must not be empty'),
        ('email', "Informe um endereço de email válido.")

    ])
    def test_empty_feild_error_message(self, field, errorMessage):
        self.browser.get(self.live_server_url + '/authors/register')
        form = self.get_form()
        self.fill_form_dummy_data(form)
        input = self.get_by_name(form, field)
        input.send_keys(" ")
        input.send_keys(Keys.ENTER)
        form = self.get_form()
        self.assertIn(errorMessage, form.text)

    def test_form_register_sucess(self):
        self.browser.get(self.live_server_url + '/authors/register')
        form = self.get_form()
        self.form_user_registers(form)
        message_success = self.browser.find_element(
            By.CLASS_NAME, 'message-success')
        self.assertIn("Your user is create, please log in",
                      message_success.text)

    def test_form_login(self):
        self.browser.get(self.live_server_url + '/authors/register')
        form = self.get_form()
        self.form_user_registers(form)
        form = self.get_form()
        self.form_user_login(form)

        message_success = self.browser.find_element(
            By.CLASS_NAME, 'message-info')
        self.assertIn("rafaelaSantana",
                      message_success.text)

    def test_form_logout(self):
        self.browser.get(self.live_server_url + '/authors/register')
        form = self.get_form()
        self.form_user_registers(form)
        form = self.get_form()
        self.form_user_login(form)

        logout = self.browser.find_element(
            By.XPATH, '//a[@aria-label="Logout"]')
        logout.send_keys(Keys.ENTER)

        form = self.browser.find_element(
            By.XPATH, "/html/body/main/div/div[2]/form")
        form.find_element(By.TAG_NAME, 'button').send_keys(Keys.ENTER)

        h2 = self.browser.find_element(By.TAG_NAME, 'h2')

        self.assertIn("Login", h2.text)
