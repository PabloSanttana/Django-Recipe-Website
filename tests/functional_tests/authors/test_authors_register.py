from .base import AuthorBaseFunctionTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parameterized import parameterized


class AuthorsRegisterFunctionTestCase(AuthorBaseFunctionTestCase):

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, "input")

        for field in fields:
            if field.is_displayed():
                field.send_keys(" " * 20)
        form.find_element(By.NAME, "email").send_keys("email@example")

    def form_user_registers(self, form):
        self.get_by_name(form, "first_name").send_keys("Rafaela")
        self.get_by_name(form, "last_name").send_keys("Santana")
        self.get_by_name(form, "username").send_keys("rafaelaSantana")
        self.get_by_name(form, "email").send_keys("rafaela@gmail.com")
        self.get_by_name(form, "password").send_keys("Ab123456789")
        self.get_by_name(form, "password2").send_keys("Ab123456789")
        self.get_by_name(form, "first_name").send_keys(Keys.ENTER)

    @parameterized.expand([
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('username', 'This field is required'),
        ('password', 'Password must not be empty'),
        ('email', "Informe um endereço de email válido.")

    ])
    def test_empty_feild_error_message(self, field, errorMessage):
        # navegar pro registro
        self.browser.get(self.live_server_url + '/authors/register')
        # selecionar o formulario
        form = self.get_form()
        # preencher com " " cada campos
        self.fill_form_dummy_data(form)
        # preencher o campo atual do parameterized
        input = self.get_by_name(form, field)
        input.send_keys(" ")
        # precionar tecla enter para enviar o formulario
        input.send_keys(Keys.ENTER)
        # pegar o novo formulario gerado com erros de validação
        form = self.get_form()
        # verificando a messagem de error do campo atual
        self.assertIn(errorMessage, form.text)

    def test_form_register_sucess(self):
        # faz o registro do usuario
        self.create_user_defualt_is_valid()
        # verificar se exite a messagem de sucesso no formualrio
        message_success = self.browser.find_element(
            By.CLASS_NAME, 'message-success')
        self.assertIn("Your user is create, please log in",
                      message_success.text)
