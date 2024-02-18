import uuid
from django.db import models
from user.models import User


class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TEXT_ANSWER = 'text'
    SINGLE_CHOICE = 'single_choice'
    MULTIPLE_CHOICE = 'multiple_choice'
    QUESTION_TYPE_CHOICES = [
        (TEXT_ANSWER, 'Текстовый ответ'),
        (SINGLE_CHOICE, 'Выбор одного из вариантов'),
        (MULTIPLE_CHOICE, 'Множественный выбор'),
    ]
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class QuizAttempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attempt_date = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True, blank=True)
