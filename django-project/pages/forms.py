from django import forms

from .models import Page
from .widgets import PageContentWidget


class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'
        widgets = {
            'content': PageContentWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['content'].widget.attrs['data-page-id'] = str(self.instance.pk)
