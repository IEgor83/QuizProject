from django.urls import path
from .views import CreateQuizAPIView, GetQuizByHashAPIView, GetQuizzesByUserAPIView

urlpatterns = [
    path('create/', CreateQuizAPIView.as_view(), name='create_quiz'),
    path('<str:hash>/', GetQuizByHashAPIView.as_view(), name='get_quiz_by_hash'),
    path('user/<str:username>/', GetQuizzesByUserAPIView.as_view(), name='get_quizzes_by_user'),
]
