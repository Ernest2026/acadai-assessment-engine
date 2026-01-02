# from django.contrib.auth.models import 
from rest_framework import serializers
from .models import AcadUser

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcadUser
        fields = ('username', 'email', 'password', 'is_student', 'is_admin')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = AcadUser.objects.create_user(**validated_data)
        return user
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)