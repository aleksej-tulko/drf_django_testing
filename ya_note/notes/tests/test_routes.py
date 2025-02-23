from http import HTTPStatus

from .test_base import TestBaseClass


class TestRoutes(TestBaseClass):

    def test_pages_availability(self):
        """
        Главная страница, регистрация, логин, логаут
        доступны анонимным юзерам.
        """
        urls = self.users_pages + (self.home_page,)
        for name in urls:
            with self.subTest(name=name):
                response = self.client.get(name)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_edit_detail_and_delete(self):
        """
        Страницы отдельной заметки, удаления и редактирования заметки
        доступны только автору заметки. Если на эти страницы попытается
        зайти другой пользователь — вернётся ошибка 404.
        """
        users_statuses = (
            (self.author, self.author_client, HTTPStatus.OK),
            (self.user, self.anon_client, HTTPStatus.NOT_FOUND)
        )
        urls = self.edit_page, self.delete_page, self.details_page
        for user, client, status in users_statuses:
            for name in urls:
                with self.subTest(user=user, name=name):
                    response = client.get(name)
                    self.assertEqual(response.status_code, status)

    def test_availability_for_auth_users(self):
        """
        Аутентифицированному пользователю доступна страница
        со списком заметок notes/, страница успешного добавления
        заметки done/, страница добавления новой заметки add/.
        """
        urls = self.add_page, self.list_page, self.success_page
        users = (
            (self.author, self.author_client),
            (self.user, self.anon_client)
        )
        for user, client in users:
            for name in urls:
                with self.subTest(user=user, name=name):
                    response = client.get(name)
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_for_anonymous_client(self):
        """
        При попытке перейти на страницу списка заметок, страницу
        успешного добавления записи, страницу добавления заметки,
        отдельной заметки, редактирования или удаления заметки
        анонимный пользователь перенаправляется на страницу логина.
        """
        urls = self.add_page, self.list_page, self.success_page,
        self.edit_page, self.details_page, self.delete_page
        for name in urls:
            with self.subTest(name=name):
                redirect_url = f'{self.login_page}?next={name}'
                response = self.client.get(name)
                self.assertRedirects(response, redirect_url)
