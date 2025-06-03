from django.contrib.auth import authenticate
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    UserRegisterSerializer, UserLoginSerializer, 
    QuestionAndAnswerSerializer, PageSerializer, PageSerializer_Detail
)
from .models import Question_and_Answer, Page
from django.contrib.auth.models import User
import cohere
from django.conf import settings

# Registration API
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

# Login API (returns JWT)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny] # allow any user to access this view
    def post(self, request):
        print(request.data)
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Page Management APIs
class PageListView(generics.ListCreateAPIView):
    serializer_class = PageSerializer
    permission_classes = [permissions.IsAuthenticated]#only authenticated users can access this view

    def get_queryset(self):
        return Page.objects.filter(user_profile=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)

class PageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PageSerializer_Detail
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Page.objects.filter(user_profile=self.request.user).prefetch_related('questions')
    

# Chat API
class ChatView(APIView):
    def post(self, request):
        user = request.user
        message = request.data.get('message')
        page_id = request.data.get('page_id')
        
        if not message:
            return Response({'detail': 'No message provided.'}, status=400)
        if not page_id:
            return Response({'detail': 'No page specified.'}, status=400)
            
        try:
            page = Page.objects.get(id=page_id, user_profile=user)
        except Page.DoesNotExist:
            return Response({'detail': 'Page not found.'}, status=404)

        # Call Cohere API
        co = cohere.Client(settings.COHERE_API_KEY)
        response = co.chat(message=message)
        # response = "This is a test response"
        bot_response = response.text if hasattr(response, 'text') else str(response)
        
        # Save question and answer
        qa = Question_and_Answer.objects.create(
            page=page,
            message=message,
            response=bot_response
        )
        
        return Response(QuestionAndAnswerSerializer(qa).data)

# Chat History API
# class ChatHistoryView(generics.ListAPIView):
#     serializer_class = QuestionAndAnswerSerializer
    
#     def get_queryset(self):
#         page_id = self.request.query_params.get('page_id')
#         if not page_id:
#             return Question_and_Answer.objects.none()
            
#         return Question_and_Answer.objects.filter(
#             page_id=page_id,
#             page__user_profile=self.request.user
#         )