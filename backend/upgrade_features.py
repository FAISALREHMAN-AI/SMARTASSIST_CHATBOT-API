import os
import sys

# 1. Models Code
models_content = """from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    message = models.TextField()
    reply = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}"
"""

# 2. Views Code (Auth, History and Chat Storage)
views_content = """import os
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
"""

# 3. New URLs Configuration
urls_content = """from django.contrib import admin
from django.urls import path
from api.views import SmartAssistChatView, RegisterView, CustomAuthToken, ChatHistoryView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="SmartAssist API with Auth & Database",
      default_version='v2',
      description="Advanced Full-Stack Chatbot API documentation with Token Auth and Chat Logs",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authenticated Routes
    path('api/chat/', SmartAssistChatView.as_view(), name='chat'),
    path('api/chat/history/', ChatHistoryView.as_view(), name='chat-history'),
    
    # Auth Endpoints
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', CustomAuthToken.as_view(), name='login'),
    
    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
"""

def patch_settings():
    settings_path = os.path.join("core", "settings.py")
    if not os.path.exists(settings_path):
        print("❌ Error: 'core/settings.py' nahi mili!")
        return False
        
    with open(settings_path, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    # 1. Add authtoken to INSTALLED_APPS
    if "rest_framework.authtoken" not in content:
        idx = content.find("INSTALLED_APPS = [")
        if idx != -1:
            end_bracket = content.find("]", idx)
            content = content[:end_bracket] + "    'rest_framework.authtoken',\n" + content[end_bracket:]
            modified = True
            print("⚙️  Added rest_framework.authtoken to INSTALLED_APPS.")

    # 2. Add REST_FRAMEWORK configurations
    if "REST_FRAMEWORK" not in content:
        content += """\n\n# DRF Configuration for Token Authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
"""
        modified = True
        print("🛡️  Configured TokenAuthentication globally in settings.py.")

    if modified:
        with open(settings_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ core/settings.py successfully updated!")
    else:
        print("ℹ️  core/settings.py already configured.")
        
    return True

def main():
    print("\n🔧 ================== SMARTASSIST FEATURES UPGRADER ==================")
    
    if not os.path.exists("manage.py"):
        print("❌ Error: Is script ko 'backend' folder me run karein jahan 'manage.py' hai.")
        sys.exit(1)

    # Patch settings.py
    if not patch_settings():
        return

    # Write api/models.py
    try:
        with open(os.path.join("api", "models.py"), "w", encoding="utf-8") as f:
            f.write(models_content)
        print("✅ api/models.py successfully updated with ChatMessage db structure!")
    except Exception as e:
        print(f"❌ Error writing models.py: {e}")
        return

    # Write api/views.py
    try:
        with open(os.path.join("api", "views.py"), "w", encoding="utf-8") as f:
            f.write(views_content)
        print("✅ api/views.py successfully written with Register, Login, History and Chat view logics!")
    except Exception as e:
        print(f"❌ Error writing views.py: {e}")
        return

    # Write core/urls.py
    try:
        with open(os.path.join("core", "urls.py"), "w", encoding="utf-8") as f:
            f.write(urls_content)
        print("✅ core/urls.py successfully updated with Token Auth API paths!")
    except Exception as e:
        print(f"❌ Error writing urls.py: {e}")
        return

    print("\n🎉 BACKEND UPGRADE COMPLETED SUCCESSFULLY!")
    print("=====================================================================\n")

if __name__ == "__main__":
    main()