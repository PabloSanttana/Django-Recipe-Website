from unittest import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.test import TestCase as djangoTestCase
from django.urls import reverse


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('first_name', 'Ex.: john'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
        ('email', 'Ex.: email@example.com'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('username', 'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'),
        ('password', (
            'Password must have at least one uppercase letter,'
            'one lowercase letter and one number.'
            'The length should be at least 8 characters'
        )),
        ('email', 'The e-mail must be valid'),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(needed, current)

    @parameterized.expand([
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Confirm Password'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),

    ])
    def test_fields_label(self, field, label):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(label, current)

# simulando um cadastro


class AuthorRegisterFormIntegrationTest(djangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'username',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@email.com',
            'password': 'Abc123456789abc123',
            'password2': 'Abc123456789abc123'
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field is required'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('password2', 'Confirm Password must not be empty'),
        ('email', 'This field is required.'),

    ])
    def test_fields_cannot_be_empty(self, field, message):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        # fallow = true seguir o curso do formulario
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(message, response.content.decode('utf-8'))
        self.assertIn(message, response.context['form'].errors.get(field))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc1234'
        url = reverse('authors:register_create')
        message = ('Password must have at least one uppercase letter,'
                   'one lowercase letter and one number.'
                   'The length should be at least 8 characters')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(message, response.context['form'].errors.get('password'))
        self.assertIn(message, response.content.decode('utf-8'))

        self.form_data['password'] = '@A123abc1234'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(
            message, response.context['form'].errors.get('password'))

    def test_password_and_password2_confirmation_are_not_equal(self):
        self.form_data['password'] = 'Abbc1234'
        self.form_data['password2'] = 'ABbc1234'
        url = reverse('authors:register_create')
        message = 'Password and password2 must be equal'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(message, response.context['form'].errors.get('password'))
        self.assertIn(
            message, response.context['form'].errors.get('password2'))
        self.assertIn(message, response.content.decode('utf-8'))

    def test_password_and_password2_confirmation_are_equal(self):
        self.form_data['password'] = 'ABbc1234'
        self.form_data['password2'] = 'ABbc1234'
        url = reverse('authors:register_create')
        message = 'Password and password2 must be equal'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(message, response.content.decode('utf-8'))

    def test_password_not_value_password(self):
        self.form_data['password'] = 'Password123'
        url = reverse('authors:register_create')
        message = 'Do not enter the Password in the password field'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(message, response.context['form'].errors.get('password'))
        self.assertIn(message, response.content.decode('utf-8'))

    def test_email_field_must_be_unique(self):
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        response = self.client.post(url, data=self.form_data, follow=True)
        message = "The email: email@email.com is already in use"
        self.assertIn(message, response.context['form'].errors.get('email'))
        self.assertIn(message, response.content.decode('utf-8'))

    def test_authors_create_can_login(self):
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username=self.form_data.get('username'),
            password=self.form_data.get('password'),
        )
        self.assertTrue(is_authenticated)

        is_authenticated = self.client.login(
            username=self.form_data.get('username'),
            password='Pasd123456',
        )
        self.assertFalse(is_authenticated)
