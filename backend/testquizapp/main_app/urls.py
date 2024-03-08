from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'main_app'

urlpatterns = [
    path('', login_required(views.TestsPageView.as_view()), name='tests-page'),
    path('create-test/', login_required(views.CreateTestView.as_view()), name='create-test'),
    path('create-question/', login_required(views.CreateQuestionView.as_view()), name='create-question'),
]