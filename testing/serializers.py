from rest_framework import serializers
from .models import Quiz, Question, Answer


class QuizSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source='creator.email', read_only=True)
    quiz_title = serializers.CharField(source='title')

    class Meta:
        model = Quiz
        fields = ['id', 'quiz_title', 'description', 'user']


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.UUIDField(source='question.id', read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'is_correct', 'question']


class QuestionSerializer(serializers.ModelSerializer):
    quiz = serializers.UUIDField(source='quiz.id', read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'quiz']
