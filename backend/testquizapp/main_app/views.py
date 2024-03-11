from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from .forms import TestQuizForm
from .models import TestQuiz, Choice, Question
from django.db.models import Count
from django.views import View

from .services import CalculateResults


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
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response

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


class TestResultsView(View):
    template_name = 'main_app/test_results.html'

    def post(self, request, test_id, *args, **kwargs):
        CalculateResults(test_id=test_id, request=request).get_results_of_test()
        return render(request, template_name=self.template_name)

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)

