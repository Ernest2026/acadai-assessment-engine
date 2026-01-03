from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Course(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Exam(models.Model):
    title = models.CharField(max_length=255)
    duration_minutes = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    metadata = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    TYPES = [('MCQ', 'Multiple Choice'), ('TEXT', 'Open Text')]
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    order_index = models.PositiveIntegerField()
    question_type = models.CharField(max_length=20, choices=TYPES)
    prompt = models.TextField()
    expected_answer = models.TextField(blank=True, null=True)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)

    class Meta:
        unique_together = ('exam', 'order_index')
        ordering = ['order_index']

class Submission(models.Model):
    STATUS = [('pending', 'Pending'), ('graded', 'Graded'), ('failed', 'Failed')]
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grading_status = models.CharField(max_length=20, choices=STATUS, default='pending')
    total_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'exam')
        indexes = [models.Index(fields=['student', 'exam'])]

class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('submission', 'question')