from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from http import HTTPStatus


User = get_user_model()


class ViewTestClass(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')

    def test_all_users_access_url(self):
        """Тестирование общедоступных страниц (core)."""
        url_status_code_access = {
            '/nonexist-page/': HTTPStatus.NOT_FOUND,
        }
        for url, status in url_status_code_access.items():
            with self.subTest(status=status):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, status)

    def test_urls_uses_correct_template(self):
        """Проверка вызываемых шаблонов для каждого адреса (core)."""
        url_templates_names = {
            '/nonexist-page/': 'core/404.html',
        }
        for url, template in url_templates_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
