from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Course, Exam, Question, Submission
from .serializers import CourseSerializer, ExamSerializer, QuestionSerializer, SubmissionSerializer
from .utils import process_submission_grading

class CourseView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExamView(APIView):
    def get(self, request):
        exams = Exam.objects.filter(is_active=True)
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionView(APIView):
    def get(self, request):
        exam_id = request.query_params.get('exam_id')
        questions = Question.objects.filter(exam_id=exam_id) if exam_id else Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubmissionView(APIView):
    # Requirement 2: Use Django's authentication system
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        submissions = Submission.objects.filter(
            student=request.user
        ).select_related('exam')
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubmissionSerializer(
            data=request.data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            submission = serializer.save()
            
            try:
                # print(submission)
                process_submission_grading(submission)
                
                return Response(
                    SubmissionSerializer(submission).data, 
                    status=status.HTTP_201_CREATED
                )
            except Exception:
                submission.grading_status = 'failed'
                submission.save()
                return Response(
                    {"error": "Internal grading error"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)