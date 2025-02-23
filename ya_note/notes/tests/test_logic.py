from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .test_base import TestBaseClass


class TestNoteCreation(TestBaseClass):

    def test_anonymous_user_cant_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        Note.objects.all().delete()
        expected_url = f'{self.login_page}?next={self.add_page}'
        response = self.client.post(self.add_page, data=self.form_data)
        self.assertRedirects(response, expected_url,
                             status_code=HTTPStatus.FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_can_create_note(self):
        """Залогиненный пользователь может создать заметку."""
        Note.objects.all().delete()
        response = self.author_client.post(
            self.add_page, data=self.form_data
        )
        self.assertRedirects(response, self.success_page,
                             status_code=HTTPStatus.FOUND)
        new_note = Note.objects.get()
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.author, self.note.author)

    def test_not_unique_slug(self):
        """Невозможно создать две заметки с одинаковым slug."""
        notes_count = Note.objects.count()
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(
            self.add_page, data=self.form_data
        )
        self.assertEqual(notes_count, Note.objects.count())
        self.assertFormError(response, 'form', 'slug',
                             errors=(self.form_data['slug'] + WARNING))

    def test_slug_not_empty(self):
        """
        Если при создании заметки не заполнен slug,
        то он формируется автоматически.
        """
        Note.objects.all().delete()
        expected_slug = slugify(self.form_data['title'])
        response = self.author_client.post(
            self.add_page, data=self.form_data
        )
        self.assertRedirects(response, self.success_page,
                             status_code=HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        self.assertEqual(note.slug, expected_slug)


class TestNoteEditDelete(TestBaseClass):

    def test_author_can_delete_note(self):
        """Для ревьювера: по-моему, вполне норм
        вначале получить кол-во записей, и полскольку удаляем одну новость,
        от этого же кол-ва  можно  просто отнять единицу
        и сравнить с тем, сколько лежит в бд в конце теста.
        """
        notes_count = Note.objects.count()
        response = self.author_client.delete(self.delete_page)
        self.assertRedirects(response, self.success_page,
                             status_code=HTTPStatus.FOUND)
        self.assertEqual(notes_count - 1, Note.objects.count())

    def test_user_cant_delete_note_of_another_user(self):
        """Пользователь не может удалять чужие заметки."""
        notes_count = Note.objects.count()
        response = self.anon_client.delete(self.delete_page)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(notes_count, Note.objects.count())

    def test_author_can_edit_note(self):
        """Пользователь может редактировать свои заметки."""
        response = self.author_client.post(
            self.edit_page, data=self.new_form_data
        )
        self.assertRedirects(response, self.success_page,
                             status_code=HTTPStatus.FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(note_from_db.title, self.new_form_data['title'])
        self.assertEqual(note_from_db.text, self.new_form_data['text'])
        self.assertEqual(note_from_db.author, self.note.author)

    def test_user_cant_edit_note_of_another_user(self):
        """Пользователь не может редактировать чужие заметки."""
        response = self.anon_client.post(
            self.edit_page, data=self.new_form_data
        )
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(note_from_db.title, self.note.title)
        self.assertEqual(note_from_db.text, self.note.text)
        self.assertEqual(note_from_db.author, self.note.author)
