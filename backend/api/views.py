import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from google import genai
from dotenv import load_dotenv
from .models import ChatMessage

load_dotenv()

# Gemini Client Initialize
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

# User Registration View
class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        
        if not username or not password:
            return Response({'error': 'Username and password are required!'}, status=status.HTTP_400_BAD_REQUEST)
            
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists!'}, status=status.HTTP_400_BAD_REQUEST)
            
        user = User.objects.create_user(username=username, password=password, email=email)
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'username': user.username,
            'message': 'User registered successfully!'
        }, status=status.HTTP_201_CREATED)

# User Login View (Custom ObtainAuthToken to return username)
class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

# Authenticated Chat View
class SmartAssistChatView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if not client:
            return Response(
                {"error": "GEMINI_API_KEY is missing from backend configuration!"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        user_message = request.data.get("message")
        if not user_message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Call Gemini
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_message,
            )
            
            # Persistent Storage: Save to SQLite Database
            ChatMessage.objects.create(
                user=request.user,
                message=user_message,
                reply=response.text
            )
            
            return Response({"reply": response.text}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Chat History Fetch View
class ChatHistoryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        messages = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
        history = []
        for msg in messages:
            history.append({
                'message': msg.message,
                'reply': msg.reply,
                'timestamp': msg.timestamp.strftime('%I:%M %p')
            })
        return Response(history, status=status.HTTP_200_OK)
