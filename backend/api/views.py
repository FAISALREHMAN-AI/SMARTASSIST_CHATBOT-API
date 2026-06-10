import os
import requests
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print(f"🔑 DEBUG: Groq API Key starts with: '{api_key[:6] if api_key else 'NOT FOUND'}'")


class SmartAssistChatView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        user_message = request.data.get("message")

        if not user_message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not api_key:
            return Response({"error": "GROQ_API_KEY missing in backend/.env file"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "user", "content": user_message}
                    ],
                },
                timeout=30,
            )

            data = response.json()

            if response.status_code != 200:
                print("❌ GROQ ERROR LOG:", data)
                return Response({"error": data}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            reply = data["choices"][0]["message"]["content"]
            return Response({"reply": reply}, status=status.HTTP_200_OK)

        except Exception as e:
            print("❌ GROQ ERROR LOG:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChatHistoryView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"history": []}, status=status.HTTP_200_OK)


class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email", "")

        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "User registered successfully",
            "token": token.key
        }, status=status.HTTP_201_CREATED)