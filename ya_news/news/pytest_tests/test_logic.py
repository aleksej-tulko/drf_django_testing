from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, NEW_COMMENT, WARNING
from news.models import Comment


pytestmark = pytest.mark.django_db

FORM_DATA = {'text': 'Новый текcт'}


def test_anonymous_user_cant_create_comment(
    client, detail_page, login_page
):
    """Анонимный пользователь не может отправить комментарий."""
    comments_count_before_test = Comment.objects.count()
    response = client.post(detail_page, data=FORM_DATA)
    expected_url = f'{login_page}?next={detail_page}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == comments_count_before_test


def test_authorised_user_can_create_comment(
    author_client, detail_page, author, news_item
):
    """Авторизованный пользователь может отправить комментарий."""
    Comment.objects.all().delete()
    comments_count_before_test = Comment.objects.count()
    author_client.post(detail_page, data=FORM_DATA)
    assert Comment.objects.count() - comments_count_before_test == 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.author == author
    assert comment.news.id == news_item.id


def test_user_behave(author_client, detail_page):
    """
    Если комментарий содержит запрещённые слова,
    он не будет опубликован, а форма вернёт ошибку.
    """
    FORM_DATA['text'] = f'Автор поста {BAD_WORDS[0]}'
    Comment.objects.all().delete()
    response = author_client.post(detail_page, data=FORM_DATA)
    assert Comment.objects.count() == 0
    assertFormError(response, 'form', 'text', errors=WARNING)


def test_authorised_user_can_edit_own_comment(
    author_client, edit_page, comment_item
):
    """Авторизованный пользователь может редактировать свои комментарии."""
    FORM_DATA['text'] = NEW_COMMENT
    author_client.post(edit_page, data=FORM_DATA)
    updated_comment = Comment.objects.get(id=comment_item.id)
    assert updated_comment.text == FORM_DATA['text']
    assert updated_comment.news == comment_item.news
    assert updated_comment.author == comment_item.author


def test_other_user_cant_edit_other_user_comment(
    not_author_client, edit_page, comment_item
):
    """Авторизованный пользователь не может редактировать чужие комментарии."""
    FORM_DATA['text'] = NEW_COMMENT
    response = not_author_client.post(edit_page, data=FORM_DATA)
    comment_from_db = Comment.objects.get(id=comment_item.id)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment_item.author == comment_from_db.author
    assert comment_item.news == comment_from_db.news
    assert comment_item.text == comment_from_db.text


def test_author_can_delete_comment(
    author_client, delete_page, comment_item
):
    """Авторизованный пользователь может удалять свои комментарии."""
    comments_count_before_test = Comment.objects.count()
    author_client.post(delete_page)
    assert not Comment.objects.filter(id=comment_item.id).exists()
    assert comments_count_before_test - Comment.objects.count() == 1


def test_other_user_cant_delete_other_user_comment(
    not_author_client, delete_page
):
    """Авторизованный пользователь не может удалять чужие комментарии."""
    comments_count_before_test = Comment.objects.count()
    response = not_author_client.post(delete_page)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comments_count_before_test
