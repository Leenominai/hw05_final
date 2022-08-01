import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.conf import settings
from http import HTTPStatus
from django.core.files.uploadedfile import SimpleUploadedFile

from posts.models import Post, Group, Comment
from posts.forms import PostForm


User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostForm()
        cls.user = User.objects.create_user(username='auth')
        cls.user_two = User.objects.create_user(username='auth_two')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='group-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост forms',
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user_two,
            text='Тестовый комментарий, который тоже длинный',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Тест: после создания поста создаётся новая запись в БД (posts)."""
        posts_count = Post.objects.count()
        form_data = {
            'text': self.post.text,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertTrue(
            Post.objects.filter(
                text=self.post.text,
            ).exists()
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': 'auth'})
        )

    def test_edit_post(self):
        """Тест: после изменения поста изменяется его записьв БД (posts)."""
        post = Post.objects.create(
            author=self.user,
            text=self.post.text,
        )
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый пост forms #2',
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', args=(post.id,)),
            data=form_data,
            follow=True
        )
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый пост forms #2',
            ).exists()
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertRedirects(response, f'/posts/{post.id}/')

    def test_create_post_with_a_pic(self):
        """Тест: после созд. c поста с карт. созд. нов. зап. в БД (posts)."""
        posts_count = Post.objects.count()
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=(
                b'\x47\x49\x46\x38\x39\x61\x02\x00'
                b'\x01\x00\x80\x00\x00\x00\x00\x00'
                b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                b'\x0A\x00\x3B'
            ),
            content_type='image/gif',
        )
        form_data = {
            'text': self.post.text,
            'image': uploaded,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertTrue(
            Post.objects.filter(
                author=self.user,
                text=self.post.text,
                image='posts/small.gif'
            ).exists()
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_title_label(self):
        """Проверка labels в form (posts)."""
        title_label = {
            'text': 'Текст поста',
            'group': 'Выбор группы по содержанию',
            'image': 'Добавление картинки',
        }
        for value, expected in title_label.items():
            with self.subTest(value=value):
                self.assertEqual(
                    PostFormTests.form.fields[value].label, expected)

    def test_title_help_text(self):
        """Проверка help_texts в form (posts)."""
        field_help_texts = {
            'text': 'Введите выше всё самое интересное',
            'group': 'Выберите выше вашу любимую группу по интересам',
            'image': 'Добавьте вашу картинку',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    PostFormTests.form.fields[value].help_text, expected)
