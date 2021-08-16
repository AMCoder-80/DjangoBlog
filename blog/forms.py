from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['parent'].label = ''
        self.fields['parent'].widget.attrs.update({
            'hidden': True
        })

    class Meta:
        model = Comment
        fields = ('parent', 'text')