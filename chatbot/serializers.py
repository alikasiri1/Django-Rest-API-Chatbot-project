from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Question_and_Answer, Page

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)#write_only=True means that the password field is not included in the response
    class Meta:
        model = User
        fields = ('username', 'password' , 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class QuestionAndAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question_and_Answer
        fields = ('id', 'message', 'response', 'created_at')
        read_only_fields = ('id', 'created_at')

class PageSerializer_Detail(serializers.ModelSerializer):
    questions = QuestionAndAnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Page
        fields = ('id', 'title', 'created_at', 'questions')
        read_only_fields = ('id', 'created_at') 

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'title', 'created_at')
        read_only_fields = ('id', 'created_at') 