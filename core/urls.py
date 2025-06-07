from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('subjects', SubjectViewSet)
router.register('quizzes', QuizViewSet)
router.register('questions', QuestionViewSet)
router.register('answers', AnswerViewSet)
router.register('scores', ScoreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
