from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
from . import api_views

app_name = 'main_app'

urlpatterns = [
    path('', login_required(views.TestsPageView.as_view()), name='tests-page'),
    path('create-test/', login_required(views.CreateTestView.as_view()), name='create-test'),
    path('create-question/', views.CreateQuestionsView.as_view(), name='create-question'),
    path('api-create-question/', api_views.GetQuestions.as_view(), name='api-create-question'),
]