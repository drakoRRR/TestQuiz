from django.contrib import admin
from.models import TestQuiz, Question, Choice, UserTestResult


@admin.register(TestQuiz)
class TestQuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'complexity')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', )


@admin.register(Choice)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_correct')


@admin.register(UserTestResult)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'test_quiz', 'score')
