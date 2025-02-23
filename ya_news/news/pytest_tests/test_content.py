import pytest
from django.conf import settings

from news.forms import CommentForm


pytestmark = pytest.mark.django_db


def test_home_page_contains_10_news_max(client, news, home_page):
    """Количество новостей на главной странице."""
    response = client.get(home_page)
    assert response.context['object_list'].count() == (
        settings.NEWS_COUNT_ON_HOME_PAGE
    )


def test_home_page_news_sorted(client, home_page):
    """
    Новости отсортированы от самой свежей к самой старой.
    Свежие новости в начале списка.
    """
    response = client.get(home_page)
    all_dates = [news.date for news in response.context['object_list']]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_detail_page_comments_sorted(client, detail_page):
    """
    Комментарии на странице отдельной новости отсортированы в
    хронологическом порядке: старые в начале списка, новые — в конце.
    """
    response = client.get(detail_page)
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_detail_page_contains_comment_form(
    author_client, detail_page
):
    """
    Авторизованному пользователю доступна форма для отправки
    омментария на странице отдельной новости.
    """
    response = author_client.get(detail_page)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


def test_anonymous_client_has_no_form(client, detail_page):
    """
    Анонимному пользователю недоступна форма для отправки
    комментария на странице отдельной новости.
    """
    response = client.get(detail_page)
    assert 'form' not in response.context
