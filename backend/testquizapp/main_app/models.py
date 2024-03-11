from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class TestQuiz(models.Model):
    """Test quiz for storing what test it is."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='user_tests', null=True, blank=True)
    complexity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        return f'{self.name}, complexity: {self.complexity}'

class Question(models.Model):
    """Question's for the test."""

    test_quiz = models.ForeignKey(TestQuiz, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='user_tests', null=True, blank=True)
    text = models.TextField()
    is_free_answer = models.BooleanField(default=False)
    is_only_one_correct_answer = models.BooleanField(default=False)
    is_few_correct_answers = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Choice(models.Model):
    """Choices for the question"""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_tests', null=True, blank=True)
    text = models.CharField(max_length=255, null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.question}, is_correct: {self.is_correct}'


class UserTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_quiz = models.ForeignKey(TestQuiz, on_delete=models.CASCADE)
    date_completed = models.DateTimeField(auto_now_add=True)
    correct_questions = models.IntegerField(default=0, blank=True, null=True)
    score = models.FloatField()
    is_passed = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.test_quiz.name} ({self.date_completed})'

class UserAnswer(models.Model):
    user_result = models.ForeignKey(UserTestResult, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    text_answer = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user_result.user.username} - {self.question.text}'