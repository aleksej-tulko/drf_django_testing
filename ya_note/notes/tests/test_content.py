from notes.forms import NoteForm
from .test_base import TestBaseClass


class TestListPage(TestBaseClass):

    def test_notes_on_list_page(self):
        """
        Отдельная заметка передаётся на страницу со списком
        заметок в списке object_list в словаре context.
        """
        response = self.author_client.get(self.list_page)
        self.assertIn(self.note, response.context['object_list'])

    def test_notes_list_own_notes(self):
        """
        В список заметок одного пользователя не попадают
        заметки другого пользователя.
        """
        users = (
            (self.author, self.author_client),
            (self.user, self.anon_client)
        )
        for user, client in users:
            with self.subTest(user=user):
                response = client.get(self.list_page)
                note_objects = response.context['object_list']
                news_count = note_objects.count()
                filtered_news_count = note_objects.filter(author=user).count()
                self.assertEqual(news_count, filtered_news_count)


class TestAddEditPage(TestBaseClass):

    def test_add_and_edit_forms(self):
        """На страницы создания и редактирования заметки передаются формы."""
        urls = self.add_page, self.edit_page
        for name in urls:
            with self.subTest(user=self.author, name=name):
                response = self.author_client.get(name)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
