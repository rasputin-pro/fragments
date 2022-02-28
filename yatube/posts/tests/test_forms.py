import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import get_object_or_404
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Group, Post
from .const import (AUTHOR, COMMENT_TEXT, EDITED_TEXT, GROUP_DESC, GROUP_SLUG,
                    GROUP_TITLE, NEW_TEXT, POST_TEXT, USER)

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):

    author = None
    post = None
    group = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USER)
        cls.author = User.objects.create_user(username=AUTHOR)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=GROUP_DESC,
        )
        cls.post = Post.objects.create(
            text=POST_TEXT,
            author=cls.author,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_user = Client()
        self.authorized_user.force_login(self.user)
        self.authorized_author = Client()
        self.authorized_author.force_login(self.author)

    def test_create_post_by_author(self):
        """Проверка формы создания поста автором."""
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded_img = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': NEW_TEXT,
            'group': PostFormTests.group.id,
            'image': uploaded_img,
        }
        response = self.authorized_author.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile',
            kwargs={'username': PostFormTests.author.username}
        ))
        post_obj_last = Post.objects.order_by('-id')[0]
        data = {
            Post.objects.count(): posts_count + 1,
            post_obj_last.text: NEW_TEXT,
            post_obj_last.group.id: PostFormTests.group.id,
            post_obj_last.image: 'posts/' + uploaded_img.__str__(),
        }
        self.check_equal(data)

    def test_create_post_invalid_form(self):
        """Невалидная форма не создаёт пост."""
        posts_count = Post.objects.count()
        form_data = {
            'text': '',
        }
        self.authorized_user.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count)

    def test_edit_post_by_author(self):
        """Проверка формы редактирования поста автором."""
        posts_count = Post.objects.count()
        form_data = {
            'text': EDITED_TEXT,
            'group': PostFormTests.group.id,
        }
        response = self.authorized_author.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': PostFormTests.post.id}
            ),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail',
            kwargs={'post_id': PostFormTests.post.id}
        ))
        post_obj = get_object_or_404(Post, id=PostFormTests.post.id)
        data = {
            Post.objects.count(): posts_count,
            post_obj.text: EDITED_TEXT,
            post_obj.group.id: PostFormTests.group.id,
        }
        self.check_equal(data)

    def test_no_post_create_by_guest(self):
        """Гость не может создать пост."""
        posts_count = Post.objects.count()
        self.client.post(
            reverse('posts:post_create'),
            data={'text': NEW_TEXT, }
        )
        self.assertEqual(Post.objects.count(), posts_count)

    def test_no_post_edit_by_guest(self):
        """Гость не может редактировать пост."""
        self.client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': PostFormTests.post.id}
            ),
            data={'text': EDITED_TEXT, }
        )
        data = {
            get_object_or_404(Post, id=PostFormTests.post.id).text: POST_TEXT,
        }
        self.check_equal(data)

    def test_no_post_edit_by_no_author(self):
        """Не автор не может редактировать пост."""
        self.authorized_user.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': PostFormTests.post.id}
            ),
            data={'text': EDITED_TEXT, }
        )
        data = {
            get_object_or_404(Post, id=PostFormTests.post.id).text: POST_TEXT,
        }
        self.check_equal(data)

    def test_no_post_comment_by_guest(self):
        """Гость не может комментировать пост."""
        count = PostFormTests.post.comments.count()
        self.client.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': PostFormTests.post.id}
            ),
            data={'text': COMMENT_TEXT, }
        )
        self.assertEqual(PostFormTests.post.comments.count(), count)

    def test_post_comment_by_user(self):
        """Зарегистрированный пользователь может комментировать пост."""
        count = PostFormTests.post.comments.count()
        self.authorized_user.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': PostFormTests.post.id}
            ),
            data={'text': COMMENT_TEXT, }
        )
        last_comment = PostFormTests.post.comments.order_by('-id')[0]
        data = {
            PostFormTests.post.comments.count(): count + 1,
            last_comment.text: COMMENT_TEXT,
        }
        self.check_equal(data)

    def check_equal(self, data):
        """
        Проверка равенства.
        Принимает словарь с проверяемыми и ожидаемыми данными.
        """
        for checked, expected in data.items():
            with self.subTest(checked=checked):
                self.assertEqual(checked, expected)
