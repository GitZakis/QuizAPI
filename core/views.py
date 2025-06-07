from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Subject, Quiz, Question, Answer, Score
from .serializers import *
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated


def home(request):
    return render(request, 'home.html')


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subject', 'created_by']

    def get_queryset(self):
        return Quiz.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['quiz']

    def get_queryset(self):
        return Question.objects.filter(quiz__created_by=self.request.user)

    def perform_create(self, serializer):
        selected_quiz = serializer.validated_data['quiz']
        if selected_quiz.created_by != self.request.user:
            raise PermissionDenied("Δεν μπορείτε να προσθέσετε ερώτηση σε quiz άλλου χρήστη.")
        serializer.save()


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['question']

    def get_queryset(self):
        return Answer.objects.filter(question__quiz__created_by=self.request.user)


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'quiz']

    def get_queryset(self):
        return Score.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
