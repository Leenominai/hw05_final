from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post, Comment, SYMBOLS_COUNT

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.user_two = User.objects.create_user(username='auth_two')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост, который очень большой',
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user_two,
            text='Тестовый комментарий, который тоже длинный',
        )

    def test_verbose_name(self):
        """Тест verbose_name в models (posts):
        Проверяем, что verbose_name в полях Post совпадает с ожидаемым.
        """
        task = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """Тест help_text в model Post (posts):
        Проверяем, что help_text в полях Post совпадает с ожидаемым."""
        task = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст поста',
            'author': 'Выбор автора',
            'group': 'Группа, к которой будет относиться пост',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task._meta.get_field(value).help_text, expected)

    def test_models_have_correct_object_names(self):
        """Тест __str__ в model Post (posts):
        Проверяем, что у моделей корректно работает __str__."""
        post_check_str = str(PostModelTest.post)
        group_check_str = str(PostModelTest.group)
        comment_check_str = str(PostModelTest.comment)
        task_list = {
            post_check_str: self.post.text[:SYMBOLS_COUNT],
            group_check_str: self.group.title,
            comment_check_str: self.comment.text[:SYMBOLS_COUNT]
        }
        for task, value in task_list.items():
            with self.subTest(task=task):
                self.assertEqual(task, value)


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

    def test_verbose_name(self):
        """Тест verbose_name в model Group (posts):
        Проверяем, что verbose_name в полях Group совпадает с ожидаемым."""
        task = GroupModelTest.group
        field_verboses = {
            'title': 'Название группы',
            'slug': 'Название в строке URL',
            'description': 'Описание группы'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """Тест help_text в model Group (posts):
        Проверяем, что help_text в полях Group совпадает с ожидаемым."""
        task = GroupModelTest.group
        field_help_texts = {
            'title': 'Введите название',
            'slug': 'Придумайте имя для group/*',
            'description': 'Введите описание группы'
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task._meta.get_field(value).help_text, expected)


class CommentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.user_two = User.objects.create_user(username='auth_two')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост, который очень большой',
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user_two,
            text='Тестовый комментарий, который тоже длинный',
        )

    def test_verbose_name(self):
        """Тест verbose_name в model Comment (posts):
        Проверяем, что verbose_name в полях Comment совпадает с ожидаемым."""
        task = CommentModelTest.comment
        field_verboses = {
            'author': 'Автор комментария',
            'text': 'Текст комментария',
            'pub_date': 'Дата публикации',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """Тест help_text в model Comment (posts):
        Проверяем, что help_text в полях Comment совпадает с ожидаемым."""
        task = CommentModelTest.comment
        field_help_texts = {
            'text': 'Добавьте Ваш комментарий',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task._meta.get_field(value).help_text, expected)
