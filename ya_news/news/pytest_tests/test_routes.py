from http import HTTPStatus

import pytest
from django.test import Client
from pytest_lazyfixture import lazy_fixture as lf
from pytest_django.asserts import assertRedirects


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'name, client, status', (
        (lf('login_page'), Client(), HTTPStatus.OK),
        (lf('logout_page'), Client(), HTTPStatus.OK),
        (lf('signup_page'), Client(), HTTPStatus.OK),
        (lf('home_page'), Client(), HTTPStatus.OK),
        (lf('detail_page'), Client(), HTTPStatus.OK),
        (lf('edit_page'), lf('not_author_client'), HTTPStatus.NOT_FOUND),
        (lf('delete_page'), lf('not_author_client'), HTTPStatus.NOT_FOUND),
        (lf('edit_page'), lf('author_client'), HTTPStatus.OK),
        (lf('delete_page'), lf('author_client'), HTTPStatus.OK)
    ),
)
def test_pages_avialability_for_anon_and_auth_users(
        name, client, status
):
    """
    Главная страница доступна анонимному пользователю.

    Страницы регистрации пользователей, входа в учётную
    запись и выхода из неё доступны анонимным пользователям.

    Страница отдельной новости доступна анонимному пользователю

    Страницы удаления и редактирования комментария
    доступны автору комментария.

    Авторизованный пользователь не может зайти на страницы
    редактирования или удаления чужих комментариев
    (возвращается ошибка 404).
    """
    response = client.get(name)
    assert response.status_code == status


@pytest.mark.parametrize(
    'name', (
        (lf('edit_page')),
        (lf('delete_page'))
    ),
)
def test_redirect_availability_for_anonymous_users(
    name, login_page, client
):
    """При попытке перейти на страницу редактирования или удаления
    комментария анонимный пользователь перенаправляется
    на страницу авторизации.
    """
    response = client.get(name)
    expected_url = f'{login_page}?next={name}'
    assertRedirects(response, expected_url)
