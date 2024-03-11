from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from main_app.models import TestQuiz, Question, Choice, UserTestResult

from rest_framework import status

class CreateTestViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_create_test_view(self):
        """Test create test by user."""
        data = {
            'name': 'Test Name',
            'description': 'Test Description',
            'complexity': 5,
        }

        response = self.client.post(reverse('main_app:create-test'), data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(TestQuiz.objects.filter(name='Test Name').exists())
        self.assertTrue(TestQuiz.objects.filter(user=self.user).exists())


class TestResultsViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.test_quiz_id = TestQuiz.objects.create(
            name='Test name',
            description='test description',
            complexity=7,
            user=self.user
        ).id

        self.question1 = Question.objects.create(
            test_quiz_id=self.test_quiz_id,
            text='Question 1',
            is_only_one_correct_answer=True
        )
        self.question2 = Question.objects.create(
            test_quiz_id=self.test_quiz_id,
            text='Question 1',
            is_few_correct_answers=True
        )
        self.question3 = Question.objects.create(
            test_quiz_id=self.test_quiz_id,
            text='Question 1',
            is_free_answer=True
        )

        self.answer1 = Choice.objects.create(
            question=self.question1,
            is_correct=True,
            text='Answer 1'
        )
        self.answer2 = Choice.objects.create(
            question=self.question1,
            is_correct=False,
            text='Answer 2'
        )

        self.answer3 = Choice.objects.create(
            question=self.question2,
            is_correct=True,
            text='Answer 3'
        )
        self.answer4 = Choice.objects.create(
            question=self.question2,
            is_correct=True,
            text='Answer 4'
        )
        self.answer5 = Choice.objects.create(
            question=self.question2,
            is_correct=False,
            text='Answer 5'
        )

        self.answer6 = Choice.objects.create(
            question=self.question3,
            is_correct=True,
            text='Answer 6'
        )

    def test_get_results_all_right(self):
        """Test when user passes the test and get the results(all answers are correct)."""

        payload = {
            f'user_answer_{self.question1.id}': self.answer1.id,  # +1 score
            f'user_answer_{self.question2.id}': [self.answer3.id, self.answer4.id],  # +2 score
            f'user_answer_{self.question3.id} {self.answer6.id}': 'Answer 6'  # +2 score
        }

        response = self.client.post(reverse('main_app:test-results', args=[self.test_quiz_id]), data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(UserTestResult.objects.filter(user=self.user, test_quiz_id=self.test_quiz_id).exists())
        self.assertEquals(UserTestResult.objects.get(user=self.user, test_quiz_id=self.test_quiz_id).score, 5)
        self.assertEquals(UserTestResult.objects.get(user=self.user, test_quiz_id=self.test_quiz_id).correct_questions, 3)

    def test_get_results_with_mistake(self):
        """Test when user passes the test and get the results(one mistake)."""

        payload = {
            f'user_answer_{self.question1.id}': self.answer2.id,  # +0 score
            f'user_answer_{self.question2.id}': [self.answer3.id, self.answer4.id],  # +2 score
            f'user_answer_{self.question3.id} {self.answer6.id}': 'Answer 6'  # +2 score
        }

        response = self.client.post(reverse('main_app:test-results', args=[self.test_quiz_id]), data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(UserTestResult.objects.filter(user=self.user, test_quiz_id=self.test_quiz_id).exists())
        self.assertEquals(UserTestResult.objects.get(user=self.user, test_quiz_id=self.test_quiz_id).score, 4)
        self.assertEquals(UserTestResult.objects.get(user=self.user, test_quiz_id=self.test_quiz_id).correct_questions, 2)


