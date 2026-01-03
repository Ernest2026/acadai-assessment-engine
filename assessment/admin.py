from django.contrib import admin
from .models import Course, Exam, Question, Submission, Answer

admin.site.register([Course, Exam, Question, Submission, Answer])