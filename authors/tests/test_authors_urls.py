from unittest import TestCase
from django.urls import reverse


class AuthorRegisterUrlsTest(TestCase):
    def test_authors_register_urls_is_correct(self):
        url = reverse('authors:register')
        self.assertEqual(url, '/authors/register/')

    def test_authors_register_create_urls_is_correct(self):
        url = reverse('authors:register_create')
        self.assertEqual(url, '/authors/register/create/')

    def test_authors_login_urls_is_correct(self):
        url = reverse('authors:login')
        self.assertEqual(url, '/authors/login/')

    def test_authors_login_create_urls_is_correct(self):
        url = reverse('authors:login_create')
        self.assertEqual(url, '/authors/login/create/')

    def test_authors_logout_urls_is_correct(self):
        url = reverse('authors:logout')
        self.assertEqual(url, '/authors/logout/')

    def test_authors_logout_user_is_correct(self):
        url = reverse('authors:logout_user')
        self.assertEqual(url, '/authors/logout/user/')
