# notes/forms.py
from django import forms
from .models import ListNote


class NoteForm(forms.ModelForm):
    class Meta:
        model = ListNote
        fields = ['title', 'text', 'finished']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'text': forms.Textarea(attrs={'class': 'form-control box2', 'required': True}),
            'finished': forms.CheckboxInput(attrs={'class': 'checkbox-note-input'}),
        }
