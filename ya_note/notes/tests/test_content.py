from notes.forms import NoteForm
from .test_base import TestBaseClass


class TestListPage(TestBaseClass):

    def test_notes_on_list_page(self):
        """
        A specific note is passed to the list page
        inside the object_list in the context dictionary.
        """
        response = self.author_client.get(self.list_page)
        self.assertIn(self.note, response.context['object_list'])

    def test_notes_list_own_notes(self):
        """
        A user's notes list does not include notes
        from another user.
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
        """Forms are passed to the note creation and editing pages."""
        urls = self.add_page, self.edit_page
        for name in urls:
            with self.subTest(user=self.author, name=name):
                response = self.author_client.get(name)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
