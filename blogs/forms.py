from django import forms
from .models import BlogPost
from django_summernote.widgets import SummernoteWidget

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image', 'is_published']
        widgets = {
            'content': SummernoteWidget(attrs={
                'summernote': {
                    'toolbar': [
                        ['style', ['style']],
                        ['font', ['bold', 'italic', 'underline', 'clear']],
                        ['para', ['ul', 'ol', 'paragraph']],
                        ['insert', ['link', 'picture', 'video']],
                        ['view', ['fullscreen', 'codeview', 'help']],
                    ],
                    'height': '400px',
                }
            }),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'is_published': 'Publish this post'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False