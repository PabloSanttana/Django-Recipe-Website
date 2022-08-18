from .base import AuthorBaseFunctionTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AuthorsLoginFunctionTestCase(AuthorBaseFunctionTestCase):

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, "input")
        for field in fields:
            if field.is_displayed():
                field.send_keys(" " * 20)

    def form_user_login(self, form):
        self.get_by_name(form, "username").send_keys("rafaelaSantana")
        self.get_by_name(form, "password").send_keys("Ab123456789")
        form.submit()

    def test_login_form_is_invalid(self):
        # creiando um usuario
        self.create_user_defualt_is_valid()
        # selecionar o novo formulario
        form = self.get_form()
        self.get_by_name(form, "username").send_keys(" "*20)
        self.get_by_name(form, "password").send_keys(" "*20)
        form.submit()
        message_Error = self.browser.find_element(
            By.CLASS_NAME, 'message-error')
        self.assertIn("Error to validate form data.",
                      message_Error.text)

    def test_login_form_is_invalid_credentials(self):
        # creiando um usuario
        self.create_user_defualt_is_valid()
        # selecionar o novo formulario
        form = self.get_form()
        self.get_by_name(form, "username").send_keys("adasdasdasdasda")
        self.get_by_name(form, "password").send_keys("Aboiowenk124")
        form.submit()
        message_Error = self.browser.find_element(
            By.CLASS_NAME, 'message-error')
        self.assertIn("Invalid credentials.",
                      message_Error.text)

    def test_form_login(self):
        self.create_user_defualt_is_valid()
        # selecionar o novo formulario
        form = self.get_form()
        # preencher o formulario completo valores validos e enviar
        self.form_user_login(form)
        # verificar se exite a messagem de sucesso
        message_success = self.browser.find_element(
            By.CLASS_NAME, 'message-info')
        self.assertIn("rafaelaSantana",
                      message_success.text)

    def test_form_logout(self):
        self.create_user_defualt_is_valid()
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
