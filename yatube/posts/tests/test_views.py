import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.conf import settings
from http import HTTPStatus
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache

from ..models import Post, Group, Comment, Follow, POSTS_LIMIT
from ..forms import PostForm


User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.follower = User.objects.create_user(username='follower')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='group-slug',
            description='Тестовое описание',
        )
        small_gif = SimpleUploadedFile(
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
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый пост',
            image=small_gif,
        )
        cls.posts_index = reverse('posts:index')
        cls.posts_group_list = reverse(
            'posts:group_list', kwargs={'slug': cls.group.slug}
        )
        cls.posts_profile = reverse(
            'posts:profile', kwargs={'username': cls.user}
        )
        cls.posts_post_detail = reverse(
            'posts:post_detail', kwargs={'post_id': cls.post.id}
        )
        cls.posts_post_create = reverse('posts:post_create')
        cls.posts_post_edit = reverse(
            'posts:post_edit', kwargs={'post_id': cls.post.id}
        )
        cls.posts_add_comment = reverse(
            'posts:add_comment', kwargs={'post_id': cls.post.id}
        )
        cls.posts_follow_index = reverse('posts:follow_index')
        cls.posts_profile_follow = reverse(
            'posts:profile_follow', kwargs={'username': cls.post.author}
        )
        cls.posts_profile_unfollow = reverse(
            'posts:profile_unfollow', kwargs={'username': cls.post.author}
        )
        cls.follow = Follow.objects.create(
            author=cls.user,
            user=cls.follower,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.follower_client = Client()
        self.follower_client.force_login(self.follower)
        cache.clear()

    def test_pages_uses_correct_template(self):
        """Проверка вызываемых шаблонов для каждой view-функции (posts)."""
        templates_page_names = {
            self.posts_index: 'posts/index.html',
            self.posts_group_list: 'posts/group_list.html',
            self.posts_profile: 'posts/profile.html',
            self.posts_post_detail: 'posts/post_detail.html',
            self.posts_post_create: 'posts/create_post.html',
            self.posts_post_edit: 'posts/create_post.html',
            self.posts_follow_index: 'posts/follow.html',
        }
        for reverse_name, template in templates_page_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_uses_correct_context(self):
        """Тест контекста index (posts):
        Проверка использования правильного контекста для функции index.
        """
        response = self.authorized_client.get(self.posts_index)
        first_object = response.context['page_obj'][0]
        second_object = response.context.get('page_obj')[0].image
        self.assertEqual(first_object, self.post)
        self.assertEqual(second_object, self.post.image)

    def test_group_list_page_uses_correct_context(self):
        """Тест контекста group_list (posts):
        Проверка использования правильного контекста для функции group_list.
        """
        response = self.authorized_client.get(self.posts_group_list)
        first_object = response.context['page_obj'][0]
        second_object = response.context['group']
        third_object = response.context.get('page_obj')[0].image
        self.assertEqual(first_object, self.post)
        self.assertEqual(second_object, self.group)
        self.assertEqual(third_object, self.post.image)

    def test_profile_page_uses_correct_context(self):
        """Тест контекста profile (posts):
        Проверка использования правильного контекста для функции profile.
        """
        response = self.authorized_client.get(self.posts_profile)
        first_object = response.context['page_obj'][0]
        second_object = response.context['author']
        third_object = response.context.get('page_obj')[0].image
        self.assertEqual(first_object, self.post)
        self.assertEqual(second_object, self.post.author)
        self.assertEqual(third_object, self.post.image)

    def test_post_detail_page_uses_correct_context(self):
        """Тест контекста post_detail (posts):
        Проверка использования правильного контекста для функции post_detail.
        """
        response = self.authorized_client.get(self.posts_post_detail)
        first_object = response.context['post']
        second_object = response.context.get('post').id
        third_object = response.context.get('post').image
        self.assertEqual(first_object, self.post)
        self.assertEqual(second_object, self.post.id)
        self.assertEqual(third_object, self.post.image)

    def test_create_post_page_uses_correct_context(self):
        """Тест контекста create_post (posts):
        Проверка использования правильного контекста для функции create_post.
        """
        response = self.authorized_client.get(self.posts_post_create)
        first_object = response.context['form']
        self.assertIsInstance(first_object, PostForm)

    def test_post_edit_page_uses_correct_context(self):
        """Тест контекста post_edit (posts):
        Проверка использования правильного контекста для функции post_edit.
        """
        response = self.authorized_client.get(self.posts_post_edit)
        first_object = response.context['form']
        second_object = response.context['post']
        third_object = response.context.get('post').id
        fourth_object = response.context['is_edit']
        self.assertIsInstance(first_object, PostForm)
        self.assertEqual(second_object, self.post)
        self.assertEqual(third_object, self.post.id)
        self.assertTrue(fourth_object)

    def test_comment_post_auth_user(self):
        """Тест нового комментария (posts):
        Проверка добавления нового комментария авторизованным  пользователем.
        """
        comment = Comment.objects.create(
            text='Новый комментарий',
            author=self.user,
            post_id=self.post.id
        )
        self.client.post(self.posts_add_comment)
        second_object = (self.client.get(self.posts_post_detail))
        self.assertContains(second_object, comment)

    def test_user_can_follow_to_author(self):
        """Тест подписки на автора (posts):
        Проверка возможности подписки авторизованного пользователя на автора.
        """
        response = self.follower_client.get(self.posts_profile_follow)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(
            Follow.objects.filter(
                user=self.follower,
                author=self.post.author
            ).exists()
        )

    def test_follower_can_unfollow_from_author(self):
        """Тест отписки от автора (posts):
        Проверка возможности отписки авторизованного пользователя от автора.
        """
        self.follower_client.get(self.posts_profile_follow)
        response = self.follower_client.get(self.posts_profile_unfollow)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(
            Follow.objects.filter(
                user=self.follower,
                author=self.post.author
            ).exists()
        )

    def test_user_can_follow_to_himself(self):
        """Тест: Нельзя подписаться на себя (posts)."""
        response = self.authorized_client.get(self.posts_profile_follow)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(
            Follow.objects.filter(
                user=self.follower,
                author=self.post.author
            ).exists()
        )
        assert self.user.follower.count() == 0

    def test_new_posts_in_follow_list(self):
        """Тест появления нового поста у подписанных пользователей (posts).
        Проверка появления новой записи пользователя в ленте тех,
        кто на него подписан.
        """
        response = self.follower_client.get(self.posts_follow_index)
        context = response.context['page_obj'].object_list
        self.assertIn(self.post, context)

    def test_new_posts_not_in_follow_list(self):
        """Тест отсутствия нового поста у неподписанных пользователей (posts).
        Проверка отсутствия появления новой записи пользователя в ленте тех,
        кто на него не подписан.
        """
        self.follower_client.get(self.posts_profile_unfollow)
        response = self.follower_client.get(self.posts_follow_index)
        context = response.context['page_obj'].object_list
        self.assertNotIn(self.post, context)

    def test_cache_index_page(self):
        """Проверяем что главная страница кешируется на 20 секунд."""
        response_one = self.authorized_client.get(self.posts_index)
        Post.objects.create(
            text='Текст тестировки кэша',
            author=self.user,
        )
        response_two = self.authorized_client.get(self.posts_index)
        self.assertEqual(response_one.content, response_two.content)
        cache.clear()
        response_three = self.authorized_client.get(self.posts_index)
        self.assertNotEqual(response_one.content, response_three.content)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='group-slug',
            description='Тестовое описание',
        )
        posts_count = 13
        bulk_list = list()
        for _ in range(posts_count):
            bulk_list.append(
                Post(
                    author=cls.user,
                    group=cls.group,
                    text='Тестовый пост',
                )
            )
        Post.objects.bulk_create(bulk_list)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        cache.clear()

    def test_index_first_page_contains_ten_records(self):
        """Проверка: количество постов на 1 странице index равно 10"""
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), POSTS_LIMIT)

    def test_index_second_page_contains_three_records(self):
        """Проверка: на 2 странице Index должно быть три поста"""
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_group_list_first_page_contains_ten_records(self):
        """Проверка: количество постов на 1 странице group_list равно 10"""
        response = self.client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        self.assertEqual(len(response.context['page_obj']), POSTS_LIMIT)

    def test_group_list_second_page_contains_three_records(self):
        """Проверка: на 2 странице group_list должно быть три поста"""
        response = self.client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
            + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_profile_first_page_contains_ten_records(self):
        """Проверка: количество постов на 1 странице profile равно 10"""
        response = self.client.get(
            reverse('posts:profile', kwargs={'username': self.user})
        )
        self.assertEqual(len(response.context['page_obj']), POSTS_LIMIT)

    def test_profile_second_page_contains_three_records(self):
        """Проверка: на 2 странице profile должно быть три поста"""
        response = self.client.get(
            reverse('posts:profile', kwargs={'username': self.user})
            + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 3)
