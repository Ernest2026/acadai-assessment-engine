from django.urls import path
from .views import CourseView, ExamView, QuestionView, SubmissionView

urlpatterns = [
    path('courses', CourseView.as_view()),
    path('exams', ExamView.as_view()),
    path('questions', QuestionView.as_view()),
    path('submissions', SubmissionView.as_view()),
]