from http import HTTPStatus as St

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class UserURLTests(TestCase):
    user = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')

    def setUp(self):
        self.guest_client = Client()
        self.authorized_user = Client()
        self.user = UserURLTests.user
        self.authorized_user.force_login(self.user)

    def test_users_page_location_for_guest(self):
        """Доступность страниц неавторизованным пользователям."""
        url_names = {
            '/auth/logout/',
            '/auth/signup/',
            '/auth/login/',
            '/auth/password-reset/',
            '/auth/password-reset/done/',
            '/auth/reset/MQ/5y6-2d727de6f3fde18895c8/',
            '/auth/reset/done/',
        }
        for url in url_names:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, St.OK)

    def test_users_redirect_for_guest(self):
        """Редирект неавторизованных пользователей."""
        response = self.guest_client.get('/auth/password-change/')
        self.assertRedirects(
            response, '/auth/login/?next=/auth/password-change/'
        )

    def test_users_page_location_for_user(self):
        """Доступность страниц авторизованным пользователям."""
        url_names = {
            '/auth/password-change/',
            '/auth/password-change/done/',
        }
        for url in url_names:
            with self.subTest(url=url):
                response = self.authorized_user.get(url)
                self.assertEqual(response.status_code, St.OK)

    def test_users_page_template(self):
        """URL-адрес использует соответствующий шаблон."""
        temp_url_names = {
            '/auth/password-reset/': 'users/password_reset_form.html',
            '/auth/password-reset/done/': 'users/password_reset_done.html',
            '/auth/reset/MQ/5y6-2d727de6f3fde18895c8/':
                'users/password_reset_confirm.html',
            '/auth/reset/done/': 'users/password_reset_complete.html',
            '/auth/password-change/': 'users/password_change_form.html',
            '/auth/password-change/done/': 'users/password_change_done.html',
            '/auth/logout/': 'users/logged_out.html',
            '/auth/signup/': 'users/signup.html',
            '/auth/login/': 'users/login.html',
        }
        for url, template in temp_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_user.get(url)
                self.assertTemplateUsed(response, template)
