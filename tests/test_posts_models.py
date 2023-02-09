from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post
from const import (
    GROUP_DESC,
    GROUP_HELP_T,
    GROUP_SLUG,
    GROUP_TITLE,
    GROUP_V_NAME,
    LONG_TEXT,
    TEXT_HELP_T,
    TEXT_V_NAME,
    USER,
)

User = get_user_model()


class PostModelTest(TestCase):

    post = None
    user = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USER)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESC,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=LONG_TEXT,
        )

    def test_post_model_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        expected = PostModelTest.post.text[:15]
        self.assertEqual(expected, str(post))

    def test_post_model_verbose_name(self):
        """Проверяем verbose_name в учебных целях."""
        post = PostModelTest.post
        field_verboses = {
            "text": TEXT_V_NAME,
            "group": GROUP_V_NAME,
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected
                )

    def test_post_model_help_text(self):
        """Проверяем help_text в учебных целях."""
        post = PostModelTest.post
        field_help_texts = {
            "text": TEXT_HELP_T,
            "group": GROUP_HELP_T,
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected
                )
