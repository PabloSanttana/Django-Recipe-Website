from django.urls import reverse, resolve
from django.test import TestCase
from authors import views


class AuthorRegisterViewsTest(TestCase):
    def test_authors_register_view_function_is_correct(self):
        url = reverse('authors:register')
        view = resolve(url)
        self.assertIs(view.func, views.register_view)

    def test_authors_register_view_returns_status_200_ok(self):
        url = reverse('authors:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_authors_register_view_loads_correct_template(self):
        url = reverse('authors:register')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'authors/pages/register_view.html')

    def test_authors_register_create_view_returns_status_404_ok(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_authors_register_create_view_returns_status_302_ok(self):
        form_data = {
            'username': 'username',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@email.com',
            'password': 'Abc123456789abc123',
            'password2': 'Abc123456789abc123'
        }
        url = reverse('authors:register_create')
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)

    def test_authors_login_view_function_is_correct(self):
        url = reverse('authors:login')
        view = resolve(url)
        self.assertIs(view.func, views.login_view)

    def test_authors_login_view_loads_correct_template(self):
        url = reverse('authors:login')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'authors/pages/login.html')

    def test_authors_login_create_view_returns_status_404_ok(self):
        url = reverse('authors:login_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
