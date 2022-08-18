from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AuthorsLogoutTest(TestCase):
    def setUp(self, *args, **kwargs):
        User.objects.create_user(
            username='RafaelaSantana',
            first_name='Rafaela',
            last_name='Santana',
            email='Rafaela@gmail.com',
            password='Abc123456789abc123',
        )
        self.client.login(username='RafaelaSantana',
                          password='Abc123456789abc123')
        return super().setUp(*args, **kwargs)

    def test_user_to_logout_using_get_methor(self):
        url = reverse('authors:logout_user')
        response = self.client.get(url, follow=True)
        self.assertIn('Your are logged in width',
                      response.content.decode('utf-8'))
        self.assertIn(f'strong>RafaelaSantana</strong>. ',
                      response.content.decode('utf-8'))

    def test_logout_not_allowed_user_different_of_the_requisition(self):
        url = reverse('authors:logout_user')
        form_data = {
            "username": 'username',
        }
        response = self.client.post(url, data=form_data, follow=True)
        self.assertIn('Your are logged in width',
                      response.content.decode('utf-8'))
        self.assertIn(f'strong>RafaelaSantana</strong>. ',
                      response.content.decode('utf-8'))

    def test_logout_with_success(self):
        username = 'RafaelaSantana'
        url = reverse('authors:logout_user')
        form_data = {
            "username": username,
        }
        response = self.client.post(url, data=form_data, follow=True)
        self.assertNotIn('Your are logged in width',
                         response.content.decode('utf-8'))
        self.assertNotIn(f'strong>{username}</strong>. ',
                         response.content.decode('utf-8'))
