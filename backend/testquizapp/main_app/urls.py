from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
from . import api_views

app_name = 'main_app'

urlpatterns = [
    path('', login_required(views.TestsPageView.as_view()), name='tests-page'),
    path('create-test/', login_required(views.CreateTestView.as_view()), name='create-test'),
    path('create-question/', views.CreateQuestionsView.as_view(), name='create-question'),

    path('delete_test/<int:test_id>/', views.DeleteTestQuizView.as_view(), name='delete_test'),

    path('test-search/', views.TestSearchView.as_view(), name='test-search'),

    path('api-create-question/', api_views.GetQuestions.as_view(), name='api-create-question'),

    path('test-process/<int:test_id>/', views.TestProcessView.as_view(), name='test-process'),
    path('test-results/<int:test_id>/', views.TestResultsView.as_view(), name='test-results'),
    path('user-tests/', views.OwnTestsUserView.as_view(), name='user-tests'),
]