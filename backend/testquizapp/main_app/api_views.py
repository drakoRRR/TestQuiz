from rest_framework import views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Question, Choice


class GetQuestions(views.APIView):
    """Create questions with answers."""
    permission_classes = [AllowAny]

    def post(self, request):
        print(request.data)
        test_id = request.data['test_id']

        for question in request.data['questions']:
            question_id = Question.objects.create(
                test_quiz_id=test_id,
                image=question['question_image'],
                text=question['question_name'],
                is_free_answer=question['is_free_answer'],
                is_only_one_correct_answer=question['is_only_one_correct_answer'],
                is_few_correct_answers=question['is_few_correct_answers']
            ).id

            for choice in question['question_choices']:
                try:
                    Choice.objects.create(
                        question_id=question_id,
                        image=choice['choice_image'],
                        text=choice['choice_name'],
                        is_correct=choice['is_correct']
                    )
                except Exception as e:
                    return Response(e, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
