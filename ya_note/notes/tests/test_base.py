from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestBaseClass(TestCase):
    """Base class for fixtures."""

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username=settings.AUTHOR)
        cls.user = User.objects.create(username=settings.NOT_AUTHOR)
        cls.note = Note.objects.create(
            title=settings.TITLE,
            text=settings.TEXT,
            author=cls.author)
        cls.home_page = reverse('notes:home')
        cls.users_pages = (reverse('users:login'),
                           reverse('users:logout'),
                           reverse('users:signup'))
        cls.add_page = reverse('notes:add')
        cls.list_page = reverse('notes:list')
        cls.success_page = reverse('notes:success')
        cls.edit_page = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_page = reverse('notes:delete', args=(cls.note.slug,))
        cls.details_page = reverse('notes:detail', args=(cls.note.slug,))
        cls.login_page = reverse('users:login')
        cls.anon_client = cls.client_class()
        cls.anon_client.force_login(cls.user)
        cls.author_client = cls.client_class()
        cls.author_client.force_login(cls.author)
        cls.form_data = {'title': settings.TITLE, 'text': settings.TEXT}
        cls.new_form_data = {'title': 'New', 'text': 'New'}
