from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import CreationForm

User = get_user_model()


class UserFormTests(TestCase):

    form = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = CreationForm()

    def setUp(self):
        self.guest_client = Client()

    def test_create_post(self):
        """Валидная форма создает нового пользователя."""
        users_count = User.objects.count()
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "user",
            "email": "user@mail.ru",
            "password1": "tTgfwv1Mwhn81KED",
            "password2": "tTgfwv1Mwhn81KED",
        }
        response = self.guest_client.post(
            reverse("users:signup"), data=form_data, follow=True
        )
        self.assertRedirects(response, reverse("posts:index"))
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertTrue(
            User.objects.filter(
                first_name="John",
                last_name="Doe",
                username="user",
                email="user@mail.ru",
            ).exists()
        )
