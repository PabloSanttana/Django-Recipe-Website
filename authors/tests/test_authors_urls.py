from unittest import TestCase
from django.urls import reverse


class AuthorRegisterUrlsTest(TestCase):
    def test_authors_register_urls_is_correct(self):
        url = reverse('authors:register')
        self.assertEqual(url, '/authors/register/')

    def test_authors_register_create_urls_is_correct(self):
        url = reverse('authors:create')
        self.assertEqual(url, '/authors/register/create/')
