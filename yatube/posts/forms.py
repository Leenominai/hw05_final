from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group', 'image']
        labels = {
            'text': 'Текст поста',
            'group': 'Выбор группы по содержанию',
            'image': 'Добавление картинки',
        }
        help_texts = {
            'text': 'Введите выше всё самое интересное',
            'group': 'Выберите выше вашу любимую группу по интересам',
            'image': 'Добавьте вашу картинку',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Текст комментария',
        }
        help_texts = {
            'text': 'Добавьте Ваш комментарий',
        }
