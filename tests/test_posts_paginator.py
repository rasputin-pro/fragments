import math

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from yatube.settings import POSTS_PER_PAGE

from posts.models import Group, Post
from const import AUTHOR, GROUP_DESC, GROUP_SLUG, GROUP_TITLE, POST_TEXT

User = get_user_model()


class PostPaginatorTests(TestCase):

    author = None
    posts = None
    group = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username=AUTHOR)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESC,
        )
        cls.posts = []
        for i in range(0, 23):
            cls.posts.append(
                Post.objects.create(
                    text=POST_TEXT,
                    author=cls.author,
                    group=cls.group,
                )
            )

    def setUp(self):
        self.authorized_author = Client()
        self.authorized_author.force_login(self.author)
        cache.clear()

    def test_posts_paginator(self):
        """Пагинатор передаёт верное количество записей на страницу."""
        pages_count = math.ceil(Post.objects.count() / POSTS_PER_PAGE)
        posts_reminder = Post.objects.count() % POSTS_PER_PAGE
        if posts_reminder == 0:
            posts_reminder = POSTS_PER_PAGE
        reverse_names = {
            reverse("posts:index"): POSTS_PER_PAGE,
            reverse("posts:index") + f"?page={pages_count}": posts_reminder,
            reverse(
                "posts:group_list",
                kwargs={"slug": PostPaginatorTests.group.slug},
            ): POSTS_PER_PAGE,
            reverse(
                "posts:group_list",
                kwargs={"slug": PostPaginatorTests.group.slug},
            )
            + f"?page={pages_count}": posts_reminder,
            reverse(
                "posts:profile",
                kwargs={"username": PostPaginatorTests.posts[0].author},
            ): POSTS_PER_PAGE,
            reverse(
                "posts:profile",
                kwargs={"username": PostPaginatorTests.posts[0].author},
            )
            + f"?page={pages_count}": posts_reminder,
        }
        for reverse_name, count in reverse_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_author.get(reverse_name)
                self.assertEqual(len(response.context["page_obj"]), count)
