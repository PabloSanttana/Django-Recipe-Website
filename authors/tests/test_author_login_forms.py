from unittest import TestCase
from authors.forms import LoginForm
from parameterized import parameterized
from django.urls import reverse
from django.test import TestCase as djangoTestCase


class AuthorLoginUnittest(TestCase):
    @parameterized.expand([
        ('username', 'Type your username'),
        ('password', 'Your password'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = LoginForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('username', 'Username'),
        ('password', 'Password'),
    ])
    def test_fields_is_correct_label(self, field, label):
        form = LoginForm()
        current_label = form[field].field.label
        self.assertEqual(label, current_label)


class AuthorLoginFromIntegrationTest(djangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'RafaelaSantana',
            'first_name': 'Rafaela',
            'last_name': 'Santana',
            'email': 'Rafaela@gmail.com',
            'password': 'Abc123456789abc123',
            'password2': 'Abc123456789abc123'
        }
        url = reverse('authors:register_create')
        self.client.post(url, data=self.form_data, follow=True)
        return super().setUp(*args, **kwargs)

    def login_user_default(self, username, password):
        url = reverse('authors:login_create')
        form_data = {
            'username': username,
            'password': password
        }
        return self.client.post(url, data=form_data, follow=True)

    def test_login_form_is_invalid(self):
        response = self.login_user_default(username="" * 20, password="" * 20)

        self.assertIn("Error to validate form data.",
                      response.content.decode('utf-8'))

    def test_login_invalid_credentials(self):
        response = self.login_user_default(
            username="username", password="asdadasfasfdaf")

        self.assertIn("Invalid credentials.",
                      response.content.decode('utf-8'))

    def test_login_message_success(self):
        username = self.form_data.get('username')
        response = self.login_user_default(username=self.form_data.get(
            'username'), password=self.form_data.get('password'))
        self.assertIn("Your are logged in.", response.content.decode('utf-8'))
        self.assertIn('Your are logged in width',
                      response.content.decode('utf-8'))
        self.assertIn(f'strong>{username}</strong>. ',
                      response.content.decode('utf-8'))
