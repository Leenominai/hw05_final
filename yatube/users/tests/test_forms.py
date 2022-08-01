from users.forms import CreationForm
from django.contrib.auth import get_user_model
from django.test import Client, TestCase


User = get_user_model()


class UsersFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = CreationForm()

    def setUp(self):
        self.guest_client = Client()

    def test_title_label(self):
        """Проверка labels в form (users)."""
        field_label = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя',
            'email': 'Адрес электронной почты',
        }
        for value, expected in field_label.items():
            with self.subTest(value=value):
                self.assertEqual(
                    UsersFormTests.form.fields[value].label, expected)

    def test_title_help_text(self):
        """Проверка help_texts в form (users)."""
        field_help_texts = {
            'first_name': 'Введите ваше имя',
            'last_name': 'Введите вашу фамилию',
            'username': 'Придумайте имя пользователя',
            'email': 'Введите адрес электронной почты',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    UsersFormTests.form.fields[value].help_text, expected)
