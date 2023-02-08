from http import HTTPStatus as St

from django.test import Client, TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_author_page_location(self):
        """Проверяем, работу страницы /about/author/."""
        response = self.guest_client.get("/about/author/")
        self.assertEqual(response.status_code, St.OK)

    def test_tech_page_location(self):
        """Проверяем, работу страницы /about/tech/."""
        response = self.guest_client.get("/about/tech/")
        self.assertEqual(response.status_code, St.OK)

    def test_author_page_template(self):
        """about:author использует соответствующий шаблон."""
        response = self.guest_client.get(reverse("about:author"))
        self.assertTemplateUsed(response, "about/author.html")

    def test_tech_page_template(self):
        """about:tech использует соответствующий шаблон."""
        response = self.guest_client.get(reverse("about:tech"))
        self.assertTemplateUsed(response, "about/tech.html")
