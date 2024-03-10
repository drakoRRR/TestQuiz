from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from .forms import TestQuizForm, QuestionForm, ChoiceForm
from .models import TestQuiz, Choice, Question
from django.db.models import Count


class TestsPageView(ListView):
    model = TestQuiz
    template_name = 'main_app/tests_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TestsPageView, self).get_context_data()

        context['tests_qty_questions'] = dict(
            Question.objects.values('test_quiz_id').annotate(
                questions_count=Count('id')
            ).values_list('test_quiz_id', 'questions_count')
        )

        return context


class CreateTestView(CreateView):
    model = TestQuiz
    form_class = TestQuizForm
    template_name = 'main_app/create_test.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        test_id = self.object.id
        return reverse('main_app:create-question') + f'?test_id={test_id}'


class CreateQuestionsView(TemplateView):
    template_name = 'main_app/create_questions.html'


class TestProcessView(ListView):
    model = Question
    template_name = 'main_app/test_process.html'

    def get_queryset(self):
        test_id = self.kwargs.get('test_id')
        queryset = super(TestProcessView, self).get_queryset()
        return queryset.filter(test_quiz_id=test_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TestProcessView, self).get_context_data(**kwargs)

        test_id = self.kwargs.get('test_id')
        questions_ids = Question.objects.filter(test_quiz_id=test_id).values_list('id', flat=True)
        choices_dict = {question_id: Choice.objects.filter(question_id=question_id) for question_id in questions_ids}

        context['choices_to_question'] = choices_dict
        context['test_id'] = test_id

        return context


def calculate_test_results(request, test_id):  # todo Refactor code, remove logic in services and write tests for it
    if request.method == 'POST':
        score = 0

        question_ids = Question.objects.filter(test_quiz_id=test_id).values_list('id', flat=True)
        questions = Question.objects.filter(test_quiz_id=test_id).values(
            'id',
            'is_free_answer',
            'is_only_one_correct_answer',
            'is_few_correct_answers'
        )

        questions_dict = dict()
        for question in questions:
            questions_dict[question['id']] = question

        for question_id in question_ids:
            if questions_dict[question_id]['is_free_answer']:

                choice_key_id = None

                for key in dict(request.POST).keys():
                    if key.startswith(f'user_answer_{question_id} '):
                        choice_key_id = key.split()[-1]
                        break

                user_answer = request.POST[f'user_answer_{question_id} {choice_key_id}']
                choice_answer = Choice.objects.get(id=choice_key_id).text

                if user_answer.strip().lower() == choice_answer.strip().lower():
                    score += 2

                continue

            choice_answer_id = list(map(int, dict(request.POST)[f'user_answer_{question_id}']))
            for choice_id in choice_answer_id:
                is_correct = Choice.objects.get(id=choice_id).is_correct
                if is_correct:
                    score += 1

        return render(request, template_name='main_app/test_results.html')

    return render(request, template_name='main_app/test_results.html')

