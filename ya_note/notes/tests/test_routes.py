from http import HTTPStatus

from .test_base import TestBaseClass


class TestRoutes(TestBaseClass):

    def test_pages_availability(self):
        """
        The home page, registration, login, and logout
        are accessible to anonymous users.
        """
        urls = self.users_pages + (self.home_page,)
        for name in urls:
            with self.subTest(name=name):
                response = self.client.get(name)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_edit_detail_and_delete(self):
        """
        The individual note page, delete page, and edit page
        are only accessible to the note's author.
        If another user tries to access these pages,
        a 404 error is returned.
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
        An authenticated user can access the notes list page (notes/),
        the success page after adding a note (done/),
        and the new note creation page (add/).
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
        If an anonymous user attempts to access the notes list page,
        the success page after adding a note, the add note page,
        the individual note page, the edit page, or the delete page,
        they are redirected to the login page.
        """
        urls = self.add_page, self.list_page, self.success_page,
        self.edit_page, self.details_page, self.delete_page
        for name in urls:
            with self.subTest(name=name):
                redirect_url = f'{self.login_page}?next={name}'
                response = self.client.get(name)
                self.assertRedirects(response, redirect_url)
