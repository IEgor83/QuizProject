from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz, Question
from django.shortcuts import get_object_or_404


class CreateQuizAPIView(APIView):
    def get_answers(self, data, questions_id):
        for i, question in enumerate(data):
            a = question["correct_answer"]
            correct_answer = [a] if not isinstance(a, list) else a
            if "options" in question:
                for ans in question["options"]:
                    is_correct = ans in correct_answer
                    q_id = get_object_or_404(Question, id=questions_id[i].id)
                    answer_serializer = AnswerSerializer(data={
                        'answer_text': ans,
                        'is_correct': is_correct,
                        'question': q_id
                    })
                    if answer_serializer.is_valid():
                        answer_serializer.save(question=q_id)
                    else:
                        return Response(answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                if "correct_answer" in question:
                    for ans in correct_answer:
                        q_id = get_object_or_404(Question, id=questions_id[i].id)
                        answer_serializer = AnswerSerializer(data={
                            'answer_text': ans,
                            'is_correct': True,
                            'question': q_id
                        })
                        if answer_serializer.is_valid():
                            answer_serializer.save(question=q_id)
                        else:
                            return Response(answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response('OK', status=status.HTTP_201_CREATED)

    def post(self, request):
        quiz_serializer = QuizSerializer(data=request.data)
        if quiz_serializer.is_valid():
            quiz_id = quiz_serializer.save(creator=request.user).id
            quiz = get_object_or_404(Quiz, id=quiz_id)
            for question_data in request.data["questions"]:
                question_data["quiz"] = quiz
            question_serializer = QuestionSerializer(data=request.data["questions"], many=True)
            if question_serializer.is_valid():
                questions = question_serializer.save(quiz=quiz)
                return self.get_answers(request.data["questions"], questions)
            return Response(question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(quiz_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetQuizByHashAPIView(APIView):
    def get(self, request, hash):
        try:
            quiz = Quiz.objects.get(id=hash)
            serializer = QuizSerializer(quiz)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Quiz.DoesNotExist:
            return Response({'error': 'Викторина не найдена'}, status=status.HTTP_404_NOT_FOUND)


class GetQuizzesByUserAPIView(APIView):
    def get(self, request):
        quizzes = Quiz.objects.filter(creator=request.user)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
