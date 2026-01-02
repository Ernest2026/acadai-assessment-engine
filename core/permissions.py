# permissions.py
from rest_framework import permissions

class IsStudentUser(permissions.BasePermission):
    """
    Check if the token is valid (handled by IsAuthenticated) 
    AND if the user has the student role.
    """
    def has_permission(self, request, view):
        # 1. Check if user is logged in (Token is valid)
        is_authenticated = bool(request.user and request.user.is_authenticated)
        
        # 2. Check if the user's role is 'student'
        # This assumes you added 'is_student' to your Custom User Model
        is_student = getattr(request.user, 'is_student', False)
        
        return is_authenticated and is_student