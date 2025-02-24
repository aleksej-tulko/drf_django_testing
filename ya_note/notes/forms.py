from pytils.translit import slugify

from django import forms
from django.core.exceptions import ValidationError

from .models import Note

WARNING = ' - such slug already exists!'


class NoteForm(forms.ModelForm):
    """The form to create or edit notes"""

    class Meta:
        model = Note
        fields = ('title', 'text', 'slug')

    def clean_slug(self):
        cleaned_data = super().clean()
        slug = cleaned_data.get('slug')
        if not slug:
            title = cleaned_data.get('title')
            slug = slugify(title)[:100]
        if Note.objects.filter(
                slug=slug
        ).exclude(id=self.instance.pk).exists():
            raise ValidationError(slug + WARNING)
        return slug
