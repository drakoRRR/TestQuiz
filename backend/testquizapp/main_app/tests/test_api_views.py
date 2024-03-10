from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from main_app.models import TestQuiz, Question, Choice

class TestApiViews(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        test_quiz = TestQuiz.objects.create(
            name='Test name',
            description='test description',
            complexity=7
        ).id
        self.test_id = str(test_quiz)

        self.mock_data = {
            'test_id': self.test_id,
            'questions_amount': '2',
            'question_name[0]': 'Question 1',
            'question_image[0]': 'undefined',
            'question_type[0]': 'single',
            'is_free_answer[0]': 'false',
            'is_only_one_correct_answer[0]': 'true',
            'is_few_correct_answers[0]': 'false',
            'len_question_choices[0]': '3',
            'questions[0]choice_name[0]': 'Choice 1',
            'questions[0]is_correct[0]': 'true',
            'questions[0]choice_image[0]': 'undefined',
            'questions[0]choice_name[1]': 'Choice 2',
            'questions[0]is_correct[1]': 'false',
            'questions[0]choice_image[1]': 'undefined',
            'questions[0]choice_name[2]': 'Choice 3',
            'questions[0]is_correct[2]': 'false',
            'questions[0]choice_image[2]': 'undefined',
            'question_name[1]': 'Question 2',
            'question_image[1]': 'undefined',
            'question_type[1]': 'free',
            'is_free_answer[1]': 'true',
            'is_only_one_correct_answer[1]': 'false',
            'is_few_correct_answers[1]': 'false',
            'len_question_choices[1]': '1',
            'questions[1]choice_name[0]': 'Choice 4',
            'questions[1]is_correct[0]': 'true',
            'questions[1]choice_image[0]': 'undefined',
        }

    def test_post_create_question(self):
        """Test create question with payload querydict."""

        url = reverse('main_app:api-create-question')
        res = self.client.post(url, self.mock_data, format='multipart')

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        expected_question_count = 2
        self.assertEqual(Question.objects.count(), expected_question_count)

        expected_question_names = ['Question 1', 'Question 2']
        actual_question_names = Question.objects.values_list('text', flat=True)
        self.assertListEqual(list(actual_question_names), expected_question_names)

        expected_choice_count = 4
        self.assertEqual(Choice.objects.count(), expected_choice_count)

        expected_choice_names = ['Choice 1', 'Choice 2', 'Choice 3', 'Choice 4']
        actual_choice_names = Choice.objects.values_list('text', flat=True)
        self.assertListEqual(list(actual_choice_names), expected_choice_names)
