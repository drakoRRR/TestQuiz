from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'main_app'

urlpatterns = [
    path('', login_required(views.TestsPageView.as_view()), name='tests-page'),
]