from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


TEXT = 'Текст'


@pytest.fixture
def home_page():
    return reverse('news:home')


@pytest.fixture
def login_page():
    return reverse('users:login')


@pytest.fixture
def logout_page():
    return reverse('users:logout')


@pytest.fixture
def signup_page():
    return reverse('users:signup')


@pytest.fixture
def detail_page(news_item):
    return reverse('news:detail', args=(news_item.pk,))


@pytest.fixture
def edit_page(comment_item):
    return reverse('news:edit', args=(comment_item.pk,))


@pytest.fixture
def delete_page(comment_item):
    return reverse('news:delete', args=(comment_item.pk,))


@pytest.fixture
def author(django_user_model):
    """Автор."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    """Зарегистрированный юзер."""
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    """Клиент автора."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    """Клиент зарегистрированного юзера."""
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    """Генерация новостей."""
    today = datetime.today()
    News.objects.bulk_create(
        News(title=f'{TEXT}-{index}',
             text=TEXT,
             date=today - timedelta(days=index))
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def news_item(news):
    """Отдельно взятая новость."""
    return News.objects.get(id=1)


@pytest.fixture
def comments(author, news_item):
    """Генерация комментов на отдельно взятой новости."""
    for index in range(settings.COMMENTS_COUNT_ON_NEWS_PAGE):
        comments = Comment.objects.create(
            text=TEXT,
            news=news_item,
            author=author
        )
        comments.created = timezone.now() + timedelta(days=index)
        comments.save()


@pytest.fixture
def comment_item(comments, news_item):
    """Отдельно взятый коммент."""
    return Comment.objects.filter(news_id=news_item).first()
