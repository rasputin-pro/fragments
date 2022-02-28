from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Follow, Post
from .const import AUTHOR, FOLLOWER, LONG_TEXT, NEW_TEXT, USER

User = get_user_model()


class PostFollowTest(TestCase):

    author = None
    post = None
    user = None
    follower = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username=AUTHOR)
        cls.user = User.objects.create_user(username=USER)
        cls.follower = User.objects.create_user(username=FOLLOWER)
        cls.post = Post.objects.create(
            author=cls.user,
            text=LONG_TEXT,
        )
        Follow.objects.create(author=cls.author, user=cls.follower)

    def setUp(self):
        self.authorized_author = Client()
        self.authorized_author.force_login(self.author)
        self.authorized_follower = Client()
        self.authorized_follower.force_login(self.follower)
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)

    def test_user_follow(self):
        """Зарегистрированный пользователь может подписаться на автора."""
        self.authorized_user.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': PostFollowTest.author}
            )
        )
        self.assertTrue(Follow.objects.filter(
            author=self.author, user=self.user
        ).exists())

    def test_follower_unfollow(self):
        """Зарегистрированный пользователь может отписаться от автора."""
        self.authorized_follower.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': PostFollowTest.author}
            )
        )
        self.assertFalse(Follow.objects.filter(
            author=self.author, user=self.follower
        ).exists())

    def test_new_post_for_follower(self):
        """У подписанного пользователя появляется новый пост автора."""
        response_one = self.authorized_follower.get(reverse(
            'posts:follow_index'))
        form_data = {
            'text': NEW_TEXT,
        }
        self.authorized_author.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        response_two = self.authorized_follower.get(reverse(
            'posts:follow_index'))
        self.assertEqual(
            len(response_two.context['page_obj']),
            len(response_one.context['page_obj']) + 1,
        )

    def test_no_new_post_for_user(self):
        """У неподписанного пользователя нет лишних постов."""
        response_one = self.authorized_user.get(reverse(
            'posts:follow_index'))
        form_data = {
            'text': NEW_TEXT,
        }
        self.authorized_author.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        response_two = self.authorized_user.get(reverse(
            'posts:follow_index'))
        self.assertEqual(
            len(response_two.context['page_obj']),
            len(response_one.context['page_obj']),
        )

    def test_following_context(self):
        """Неподписанному пользователю following->False."""
        response = self.authorized_user.get(
            reverse(
                'posts:profile',
                kwargs={'username': PostFollowTest.author}
            )
        )
        self.assertFalse(response.context['following'])
