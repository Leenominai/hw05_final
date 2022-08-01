from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя',
            'email': 'Адрес электронной почты',
        }
        help_texts = {
            'first_name': 'Введите ваше имя',
            'last_name': 'Введите вашу фамилию',
            'username': 'Придумайте имя пользователя',
            'email': 'Введите адрес электронной почты',
        }
