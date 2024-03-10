from ast import literal_eval as li

from .models import Question, Choice


class CreateQuestionService:
    """Create question service."""

    def __init__(self, request, i):
        self.test_id = int(request.data.get('test_id'))
        self.question_name = str(request.data.get(f'question_name[{i}]'))
        self.question_image = request.data.get(f'question_image[{i}]')
        self.is_free_answer = li(
            request.data.get(f'is_free_answer[{i}]').replace('true', 'True').replace('false', 'False')
        )
        self.is_only_one_correct_answer = li(
            request.data.get(f'is_only_one_correct_answer[{i}]').replace('true', 'True').replace('false', 'False')
        )
        self.is_few_correct_answers = li(
            request.data.get(f'is_few_correct_answers[{i}]').replace('true', 'True').replace('false', 'False')
        )

    def create_question(self):
        """Create question with existing test."""
        question = Question.objects.create(
            test_quiz_id=self.test_id,
            image=self.question_image if self.question_image != 'undefined' else None,
            text=self.question_name,
            is_free_answer=self.is_free_answer,
            is_only_one_correct_answer=self.is_only_one_correct_answer,
            is_few_correct_answers=self.is_few_correct_answers
        )

        return question


class CreateChoiceService:
    """Create choice service"""

    def __init__(self, request, question, i, j):
        self.question = question
        self.choice_name = str(request.data.get(f'questions[{i}]choice_name[{j}]'))
        self.is_correct_value = li(
            request.data.get(f'questions[{i}]is_correct[{j}]').replace('true', 'True').replace('false', 'False'))
        self.choice_image = request.data.get(f'questions[{i}]choice_image[{j}]')

    def create_choice(self):
        """Create choice with existing question."""
        choice = Choice.objects.create(
            question=self.question,
            text=self.choice_name,
            is_correct=self.is_correct_value,
            image=self.choice_image if self.choice_image != 'undefined' else None
        )

        return choice


