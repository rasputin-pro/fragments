from http import HTTPStatus as St

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase

from posts.models import Group, Post
from const import AUTHOR, GROUP_DESC, GROUP_SLUG, GROUP_TITLE, POST_TEXT, USER

User = get_user_model()


class PostURLTests(TestCase):

    user = None
    author = None
    post = None
    group = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username=AUTHOR)
        cls.user = User.objects.create_user(username=USER)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESC,
        )
        cls.post = Post.objects.create(
            text=POST_TEXT,
            author=cls.author,
            group=cls.group,
        )

    def setUp(self):
        self.authorized_author = Client()
        self.authorized_user = Client()
        self.authorized_author.force_login(self.author)
        self.authorized_user.force_login(self.user)
        cache.clear()

    def test_posts_page_location_for_guest(self):
        """Доступность страниц неавторизованным пользователям."""
        url_names = {
            "/",
            f"/group/{PostURLTests.post.group.slug}/",
            f"/profile/{PostURLTests.author}/",
            f"/posts/{PostURLTests.post.id}/",
        }
        for url in url_names:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, St.OK)

    def test_posts_redirect_for_guest(self):
        """Редирект неавторизованных пользователей."""
        url_names = {
            "/create/": "/auth/login/?next=/create/",
            f"/posts/{PostURLTests.post.id}/edit/":
                f"/auth/login/?next=/posts/{PostURLTests.post.id}/edit/",
            f"/profile/{PostURLTests.author}/follow/":
                f"/auth/login/?next=/profile/"
            f"{PostURLTests.author}/follow/",
            f"/profile/{PostURLTests.author}/unfollow/":
                f"/auth/login/?next=/profile/"
            f"{PostURLTests.author}/unfollow/",
        }
        for url, redirect in url_names.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, redirect)

    def test_posts_page_location_for_user(self):
        """Страница создания поста доступна авторизованному пользователю."""
        response = self.authorized_user.get("/create/")
        self.assertEqual(response.status_code, St.OK)

    def test_posts_page_location_for_author(self):
        """Страница редактирования поста доступна автору."""
        response = self.authorized_author.get(
            f"/posts/{PostURLTests.post.id}/edit/"
        )
        self.assertEqual(response.status_code, St.OK)

    def test_posts_redirect_for_not_author(self):
        """Редирект не автора на страницу поста."""
        response = self.authorized_user.get(
            f"/posts/{PostURLTests.post.id}/edit/", follow=True
        )
        self.assertRedirects(response, f"/posts/{PostURLTests.post.id}/")

    def test_posts_page_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            "/": "posts/index.html",
            f"/group/{PostURLTests.post.group.slug}/": "posts/group_list.html",
            f"/profile/{PostURLTests.author}/": "posts/profile.html",
            f"/posts/{PostURLTests.post.id}/": "posts/post_detail.html",
            "/create/": "posts/post_edit.html",
            f"/posts/{PostURLTests.post.id}/edit/": "posts/post_edit.html",
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_author.get(url)
                self.assertTemplateUsed(response, template)

    def test_unknown_page_404_error(self):
        """Ошибка 404 на несуществующей странице."""
        response = self.client.get("/unexisting-page/")
        self.assertEqual(response.status_code, St.NOT_FOUND)

    def test_custom_template_404_error(self):
        """Страница 404 использует переопределенный шаблон."""
        response = self.client.get("/unexisting-page/")
        self.assertTemplateUsed(response, "core/404.html")
