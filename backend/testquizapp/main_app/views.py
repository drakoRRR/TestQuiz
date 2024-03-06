from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class TestsPageView(TemplateView):
    template_name = 'main_app/tests_page.html'
