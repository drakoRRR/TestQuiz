from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from .forms import TestQuizForm, QuestionForm, ChoiceForm
from .models import TestQuiz, Choice, Question


class TestsPageView(ListView):
    model = TestQuiz
    template_name = 'main_app/tests_page.html'


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
