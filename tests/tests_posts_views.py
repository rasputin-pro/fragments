import shutil
import tempfile

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Group, Post
from .const import (
    AUTHOR,
    GROUP_DESC,
    GROUP_DESC_2,
    GROUP_SLUG,
    GROUP_SLUG_2,
    GROUP_TITLE,
    GROUP_TITLE_2,
    POST_TEXT,
    POST_TITLE,
)

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostViewsTests(TestCase):

    author = None
    post = None
    group = None
    group_2 = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username=AUTHOR)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESC,
        )
        cls.group_2 = Group.objects.create(
            title=GROUP_TITLE_2,
            slug=GROUP_SLUG_2,
            description=GROUP_DESC_2,
        )
        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00"
            b"\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00"
            b"\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        uploaded_img = SimpleUploadedFile(
            name="small.gif", content=small_gif, content_type="image/gif"
        )
        cls.post = Post.objects.create(
            author=cls.author,
            title=POST_TITLE,
            text=POST_TEXT,
            group=cls.group,
            image=uploaded_img,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_author = Client()
        self.authorized_author.force_login(self.author)
        cache.clear()

    def test_posts_page_template(self):
        """posts: использует соответствующий шаблон."""
        templates_pages_names = {
            reverse("posts:index"): "posts/index.html",
            reverse(
                "posts:group_list",
                kwargs={"slug": PostViewsTests.post.group.slug},
            ): "posts/group_list.html",
            reverse(
                "posts:profile",
                kwargs={"username": PostViewsTests.post.author},
            ): "posts/profile.html",
            reverse(
                "posts:post_detail", kwargs={"post_id": PostViewsTests.post.id}
            ): "posts/post_detail.html",
            reverse("posts:post_create"): "posts/post_edit.html",
            reverse(
                "posts:post_edit", kwargs={"post_id": PostViewsTests.post.id}
            ): "posts/post_edit.html",
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_author.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_posts_list_context(self):
        """posts: со списком сформированы с правильным контекстом."""
        reverse_names = {
            reverse("posts:index"),
            reverse(
                "posts:group_list", kwargs={"slug": PostViewsTests.group.slug}
            ),
            reverse(
                "posts:profile",
                kwargs={"username": PostViewsTests.post.author},
            ),
        }
        for reverse_name in reverse_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_author.get(reverse_name)
                first_obj = response.context["page_obj"][0]
                data = {
                    first_obj.id: PostViewsTests.post.id,
                    first_obj.title: PostViewsTests.post.title,
                    first_obj.text: PostViewsTests.post.text,
                    first_obj.author: PostViewsTests.post.author,
                    first_obj.group: PostViewsTests.post.group,
                    first_obj.image: PostViewsTests.post.image,
                }
                self.check_equal(data)

    def test_posts_group_context(self):
        """posts:group_list сформирован с правильным контекстом."""
        response = self.authorized_author.get(
            reverse(
                "posts:group_list", kwargs={"slug": PostViewsTests.group.slug}
            )
        )
        group = response.context["group"]
        data = {
            group.title: PostViewsTests.group.title,
            group.slug: PostViewsTests.group.slug,
            group.description: PostViewsTests.group.description,
        }
        self.check_equal(data)

    def test_posts_profile_context(self):
        """posts:profile сформирован с правильным контекстом."""
        response = self.authorized_author.get(
            reverse(
                "posts:profile",
                kwargs={"username": PostViewsTests.post.author},
            )
        )
        data = {
            response.context["author"].id: PostViewsTests.author.id,
            response.context["count"]: len(Post.objects.all()),
        }
        self.check_equal(data)

    def test_posts_post_detail_context(self):
        """posts:post_detail сформирован с правильным контекстом."""
        response = self.authorized_author.get(
            reverse(
                "posts:post_detail", kwargs={"post_id": PostViewsTests.post.id}
            )
        )
        post_obj = response.context["post"]
        title = response.context["title"]
        count = response.context["count"]
        data = {
            post_obj.title: PostViewsTests.post.title,
            post_obj.text: PostViewsTests.post.text,
            post_obj.author: PostViewsTests.post.author,
            post_obj.group: PostViewsTests.post.group,
            post_obj.image: PostViewsTests.post.image,
            title: PostViewsTests.post.text[:30],
            count: len(Post.objects.all()),
        }
        self.check_equal(data)

    def test_posts_post_create_context(self):
        """posts: с формой сформирован с правильным контекстом."""
        reverse_names = {
            reverse("posts:post_create"),
            reverse(
                "posts:post_edit",
                kwargs={"post_id": PostViewsTests.post.id},
            ),
        }
        form_fields = {
            "title": forms.fields.CharField,
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }
        for rev in reverse_names:
            response = self.authorized_author.get(rev)
            for checked, expected in form_fields.items():
                with self.subTest(checked=checked):
                    form_field = response.context.get("form").fields.get(
                        checked
                    )
                    self.assertIsInstance(form_field, expected)

    def test_posts_post_edit_context(self):
        """posts:post_edit сформирован с правильным контекстом."""
        response = self.authorized_author.get(
            reverse(
                "posts:post_edit",
                kwargs={"post_id": PostViewsTests.post.id},
            )
        )
        post_obj = response.context.get("post")
        is_edit = response.context.get("is_edit")
        data = {
            post_obj.text: PostViewsTests.post.text,
            post_obj.author: PostViewsTests.post.author,
            post_obj.group: PostViewsTests.post.group,
            is_edit: True,
        }
        self.check_equal(data)

    def test_posts_post_on_correct_page(self):
        """Пост отображается там где должен."""
        reverse_names = {
            reverse("posts:index"),
            reverse(
                "posts:group_list", kwargs={"slug": PostViewsTests.group.slug}
            ),
            reverse(
                "posts:profile",
                kwargs={"username": PostViewsTests.post.author},
            ),
        }
        for rev in reverse_names:
            response = self.authorized_author.get(rev)
            obj = response.context.get("page_obj").object_list
            with self.subTest(rev=rev):
                self.assertIn(PostViewsTests.post, obj)

    def test_posts_post_not_in_alien_group(self):
        """Пост отсутствует в группе, к которой не относится."""
        response = self.authorized_author.get(
            reverse(
                "posts:group_list",
                kwargs={"slug": PostViewsTests.group_2.slug},
            )
        )
        obj = response.context.get("page_obj").object_list
        self.assertNotIn(PostViewsTests.post, obj)

    def check_equal(self, data):
        """
        Проверка контекста.
        Принимает словарь с проверяемыми и ожидаемыми данными.
        """
        for checked, expected in data.items():
            with self.subTest(checked=checked):
                self.assertEqual(checked, expected)
