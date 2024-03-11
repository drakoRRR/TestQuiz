from django.contrib import auth, messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from django.contrib.auth.models import User

from main_app.models import UserTestResult, TestQuiz
from main_app.services import get_max_possible_score


# Create your views here.
class LoginUserView(LoginView):
    """Authenticate user view."""
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error with username or password, check again !')
        return super().form_invalid(form)


class RegistrationView(CreateView):
    """Register user view."""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('')

    def form_valid(self, form):
        response = super().form_valid(form)
        auth.login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error with username or password, check again !')
        return super().form_invalid(form)


class ProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['test_history'] = UserTestResult.objects.filter(user=self.request.user)

        test_ids = TestQuiz.objects.all().values_list('id', flat=True)
        max_possible_score_dict = dict()

        for test_id in test_ids:
            max_possible_score_dict[test_id] = get_max_possible_score(test_id)

        context['max_possible_score_dict'] = max_possible_score_dict

        return context

