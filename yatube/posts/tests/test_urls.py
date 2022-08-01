from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from http import HTTPStatus

from ..models import Post, Group

User = get_user_model()


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='group-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_all_users_access_url(self):
        """Тестирование общедоступных страниц (posts)."""
        url_status_code_access = {
            '/': HTTPStatus.OK,
            f'/group/{self.group.slug}/': HTTPStatus.OK,
            f'/profile/{self.user}/': HTTPStatus.OK,
            f'/posts/{self.post.id}/': HTTPStatus.OK,
            '/unexisting_page/': HTTPStatus.NOT_FOUND,
        }
        for url, status in url_status_code_access.items():
            with self.subTest(status=status):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, status)

    def test_auth_users_access_url(self):
        """Тестирование страниц авторизованных пользователей (posts)."""
        url_status_code_access = {
            '/create/': HTTPStatus.OK,
            f'/posts/{self.post.id}/edit/': HTTPStatus.OK,
            f'/posts/{self.post.id}/comment/': HTTPStatus.FOUND,
            '/follow/': HTTPStatus.OK,
        }
        for url, status in url_status_code_access.items():
            with self.subTest(status=status):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, status)

    def test_url_redirect_no_author_from_edit_any_post_to_that_post(self):
        """Тест: При попытке неавтора ред. пост, редир. на тот пост (posts)"""
        if self.user != self.post.author:
            url_redirects = {
                f'/posts/{self.post.id}/edit/': f'/posts/{self.post.id}/',
            }
            for url, redirect_url in url_redirects.items():
                with self.subTest(redirect_url=redirect_url):
                    response = self.guest_client.get(url, follow=True)
                    self.assertRedirects(response, redirect_url)

    def test_url_redirect_anonymous_on_admin_login(self):
        """Страница перенаправит анонимного польз. страницу логина (posts)"""
        url_redirects = {
            '/create/': '/auth/login/?next=' + '/create/',
            f'/posts/{self.post.id}/comment/':
                '/auth/login/?next=' + f'/posts/{self.post.id}/comment/',
        }
        for url, redirect_url in url_redirects.items():
            with self.subTest(redirect_url=redirect_url):
                response = self.guest_client.get(url, follow=True)
                self.assertRedirects(response, redirect_url)

    def test_urls_uses_correct_template(self):
        """Проверка вызываемых шаблонов для каждого адреса (posts)."""
        url_templates_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user}/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            f'/posts/{self.post.id}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
            '/follow/': 'posts/follow.html',
        }
        for url, template in url_templates_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
