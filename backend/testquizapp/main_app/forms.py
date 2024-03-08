from django import forms
from .models import TestQuiz

class TestQuizForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'required': 'true'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'required': 'true'
    }))
    complexity = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'min': '1',
        'max': '10',
        'required': 'true'
    }))
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'class': 'form-control-file'
    }), required=False)

    class Meta:
        model = TestQuiz
        fields = ['name', 'description', 'complexity', 'image']
