from rest_framework import serializers
from .models import Course, Exam, Question, Submission, Answer

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'exam', 'order_index', 'question_type', 'prompt', 'max_score']

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'duration_minutes', 'course', 'metadata', 'questions']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'answer_text']

class SubmissionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, write_only=True)
    
    class Meta:
        model = Submission
        fields = ['id', 'exam', 'submitted_at', 'grading_status', 'total_score', 'answers']
        read_only_fields = ['grading_status', 'total_score', 'submitted_at']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        submission = Submission.objects.create(
            student=self.context['request'].user, 
            **validated_data
        )
        
        answer_instances = [
            Answer(submission=submission, **data) for data in answers_data
        ]
        Answer.objects.bulk_create(answer_instances)
        return submission