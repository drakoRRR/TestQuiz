from django.contrib import admin
from.models import TestQuiz


@admin.register(TestQuiz)
class TestQuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'complexity')
