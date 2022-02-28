from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from ..models import Post
from .const import AUTHOR, POST_TEXT

User = get_user_model()


class PostCacheTests(TestCase):

    author = None
    post = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username=AUTHOR)
        cls.post = Post.objects.create(
            author=cls.author,
            text=POST_TEXT,
        )

    def test_cache_index_page_obj(self):
        """Объекты главной страницы кэшируются"""
        response_one = self.client.get(reverse('posts:index')).content
        self.post.delete()
        response_two = self.client.get(reverse('posts:index')).content
        self.assertEqual(response_one, response_two)
        cache.clear()
        response_three = self.client.get(reverse('posts:index')).content
        self.assertNotEqual(response_two, response_three)
