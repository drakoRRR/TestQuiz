from django import forms
from .models import TestQuiz, Question, Choice


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
        'class': 'form-control-file',
        'type': 'file',
        'accept': 'image/*',
        'onchange': 'displayFileName(this)'
    }), required=False)

    class Meta:
        model = TestQuiz
        fields = ['name', 'description', 'complexity', 'image']


class QuestionForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'required': 'true',
        'name': 'questions[]'
    }))
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'class': 'file-input-wrapper mt-2',
        'type': 'file',
        'id': 'questionImage',
        'accept': 'image/*',
        'onchange': 'displayFileName(this)',
        'name': 'questionImages[]'
    }), required=False)
    is_free_answer = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control',
        'name': 'questionTypes[]',
    }), choices=[('free', 'Вільна відповідь'), ('single', 'Одна правильна відповідь'), ('multiple', 'Декілька правильних відповідей')])

    class Meta:
        model = Question
        fields = ['image', 'text', 'is_free_answer', 'is_only_one_correct_answer', 'is_few_correct_answers']

    def clean(self):
        cleaned_data = super().clean()
        is_free_answer = cleaned_data.get('is_free_answer')

        if is_free_answer == 'free':
            cleaned_data['is_free_answer'] = True
        elif is_free_answer == 'single':
            cleaned_data['is_only_one_correct_answer'] = True
        elif is_free_answer == 'multiple':
            cleaned_data['is_few_correct_answers'] = True

        return cleaned_data


class ChoiceForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'required': 'true',
        'name': 'choices[]'
    }), required=False)
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'class': 'file-input-wrapper mt-2',
        'type': 'file',
        'id': 'choiceImage',
        'accept': 'image/*',
        'onchange': 'displayFileName(this)',
        'name': 'choiceImages[]'
    }), required=False)
    is_correct = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input',
        'name': 'is_correct[]'
    }), required=False)

    class Meta:
        model = Choice
        fields = ['image', 'text', 'is_correct']

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        image = cleaned_data.get('image')

        if not text and not image:
            raise forms.ValidationError('Either text or image is required.')

        return cleaned_data
