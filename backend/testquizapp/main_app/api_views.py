from rest_framework import views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Question, Choice

from ast import literal_eval as li


class GetQuestions(views.APIView):  # todo Refactor create service
    """Create questions with answers."""
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        print(request.data)
        test_id = int(request.data.get('test_id'))
        questions_count = request.data.get('questions_amount')

        for i in range(int(questions_count)):
            question_name = str(request.data.get(f'question_name[{i}]'))
            question_image = request.data.get(f'question_image[{i}]')
            is_free_answer = li(request.data.get(f'is_free_answer[{i}]').replace('true', 'True').replace('false', 'False'))
            is_only_one_correct_answer = li(request.data.get(f'is_only_one_correct_answer[{i}]').replace('true', 'True').replace('false', 'False'))
            is_few_correct_answers = li(request.data.get(f'is_few_correct_answers[{i}]').replace('true', 'True').replace('false', 'False'))

            question = Question.objects.create(
                test_quiz_id=test_id,
                image=question_image if question_image != 'undefined' else None,
                text=question_name,
                is_free_answer=is_free_answer,
                is_only_one_correct_answer=is_only_one_correct_answer,
                is_few_correct_answers=is_few_correct_answers
            )

            len_choices = int(request.data.get(f'len_question_choices[{i}]'))

            for j in range(len_choices):
                choice_name = str(request.data.get(f'questions[{i}]choice_name[{j}]'))
                is_correct_value = li(request.data.get(f'questions[{i}]is_correct[{j}]').replace('true', 'True').replace('false', 'False'))
                choice_image = request.data.get(f'questions[{i}]choice_image[{j}]')

                try:
                    Choice.objects.create(
                        question=question,
                        text=choice_name,
                        is_correct=is_correct_value,
                        image=choice_image if choice_image != 'undefined' else None
                    )
                except Exception as e:
                    return Response(e, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
