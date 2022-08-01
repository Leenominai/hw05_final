from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from ..forms import CreationForm

User = get_user_model()


class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """Проверка вызываемых шаблонов для каждой view-функции (users)."""
        templates_page_names = {
            reverse('users:signup'): 'users/signup.html',
            reverse('users:login'): 'users/login.html',
            reverse('users:password_change_form'):
                'users/password_change_form.html',
            reverse('users:password_change_done'):
                'users/password_change_done.html',
            reverse('users:password_reset_form'):
                'users/password_reset_form.html',
            reverse('users:password_reset_done'):
                'users/password_reset_done.html',
            reverse(
                'users:password_reset_confirm',
                kwargs={'uidb64': '123', 'token': '345'}
            ): 'users/password_reset_confirm.html',
            reverse('users:password_reset_complete'):
                'users/password_reset_complete.html',
            reverse('users:logout'):
                'users/logged_out.html',
        }
        for reverse_name, template in templates_page_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_signup_page_uses_correct_context(self):
        """Проверка использования правильного контекста signup (users)."""
        response = self.authorized_client.get(reverse('users:signup'))
        first_object = response.context['form']
        self.assertIsInstance(first_object, CreationForm)
