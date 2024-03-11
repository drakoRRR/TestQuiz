from rest_framework import views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Question, Choice

from .services import CreateQuestionService, CreateChoiceService


class GetQuestions(views.APIView):
    """Create questions with answers."""
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        questions_count = request.data.get('questions_amount')

        for i in range(int(questions_count)):
            question = CreateQuestionService(request, i).create_question()

            len_choices = int(request.data.get(f'len_question_choices[{i}]'))

            for j in range(len_choices):
                CreateChoiceService(request, question, i, j).create_choice()

        return Response(status=status.HTTP_200_OK)
