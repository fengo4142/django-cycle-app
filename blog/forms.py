from django import forms
from django.contrib import admin
from tinymce.widgets import TinyMCE


class BlogAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BlogAdminForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = TinyMCE(attrs={'cols': 80, 'rows': 30})
