from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from .forms import TestQuizForm
from .models import TestQuiz


class TestsPageView(ListView):
    model = TestQuiz
    template_name = 'main_app/tests_page.html'


class CreateTestView(CreateView):
    model = TestQuiz
    form_class = TestQuizForm
    template_name = 'main_app/create_test.html'
    success_url = reverse_lazy('main_app:create-question')

    def form_valid(self, form):
        return super().form_valid(form)


class CreateQuestionView(TemplateView):
    # model = TestQuiz
    template_name = 'main_app/create_questions.html'
