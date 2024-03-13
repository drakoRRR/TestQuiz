from ast import literal_eval as li

from .models import Question, Choice, UserTestResult

from .documents import TestQuizDocument


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


class CalculateResults:
    """Calculate score in test."""

    def __init__(self, test_id, request):
        self.score = 0
        self.correct_questions = 0
        self.test_id = test_id
        self.request = request
        self.question_ids = Question.objects.filter(test_quiz_id=test_id).values_list('id', flat=True)
        self.questions_dict = self.get_question_dict()

    def get_results_of_test(self):
        """Get total results(score) of test."""
        for question_id in self.question_ids:
            if self.questions_dict[question_id]['is_free_answer']:

                self.calculate_free_answer(question_id)
                continue

            self.calculate_few_or_one_answers(question_id)

        return self.save_results()

    def save_results(self):
        """Save results of test in model UserTestResult."""
        return UserTestResult.objects.create(
            user_id=self.request.user.id,
            test_quiz_id=self.test_id,
            score=self.score,
            correct_questions=self.correct_questions
        )

    def calculate_free_answer(self, question_id):
        """Calculate point of free answer."""
        choice_key_id = None

        for key in dict(self.request.POST).keys():
            if key.startswith(f'user_answer_{question_id} '):
                choice_key_id = key.split()[-1]
                break

        user_answer = self.request.POST[f'user_answer_{question_id} {choice_key_id}']
        choice_answer = Choice.objects.get(id=choice_key_id).text

        if user_answer.strip().lower() == choice_answer.strip().lower():
            self.score += 2
            self.correct_questions += 1

    def calculate_few_or_one_answers(self, question_id):
        """Calculate point of few options type question and one correct type question."""
        choice_answer_id = list(map(int, dict(self.request.POST)[f'user_answer_{question_id}']))

        if len(choice_answer_id) == 1:
            is_correct = Choice.objects.get(id=choice_answer_id[0]).is_correct
            if is_correct:
                self.score += 1
                self.correct_questions += 1
        else:
            coefficient = 2 / len(choice_answer_id)
            score_by_question = 0
            for choice_id in choice_answer_id:
                is_correct = Choice.objects.get(id=choice_id).is_correct
                if is_correct:
                    score_by_question += coefficient

            if score_by_question > 0.8:
                self.score += score_by_question
                self.correct_questions += 1

    def get_question_dict(self):
        """Get question dict with type of answers."""
        questions = Question.objects.filter(test_quiz_id=self.test_id).values(
            'id',
            'is_free_answer',
            'is_only_one_correct_answer',
            'is_few_correct_answers'
        )

        questions_dict = dict()
        for question in questions:
            questions_dict[question['id']] = question

        return questions_dict


def get_max_possible_score(test_id=None):
    """Get max possible score on test"""

    max_possible_score = 0

    for question in Question.objects.filter(test_quiz_id=test_id):
        if question.is_free_answer or question.is_few_correct_answers:
            max_possible_score += 2
            continue
        if question.is_only_one_correct_answer:
            max_possible_score += 1

    return max_possible_score


def get_ids_to_search(search_query):
    """Get ids to search from elasticsearch."""
    s = TestQuizDocument.search().filter('match', name=search_query).to_queryset().order_by('name').distinct('name')
    tests_names = []
    test_ids = []

    for hit in s:
        if hit.name not in tests_names:
            test_ids.append(hit.id)
            tests_names.append(hit.name)

    return test_ids
