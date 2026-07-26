import os
from openai import OpenAI
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .serializers import ChatMessageSerializer, UserRegisterSerializer

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY:
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=GROQ_API_KEY
    )
else:
    client = None


class SmartAssistChatView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ChatMessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_message = serializer.validated_data.get("message")

        if not client:
            return Response(
                {"reply": "Server configuration error: GROQ_API_KEY is not set."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": user_message}]
            )
            return Response(
                {"reply": response.choices[0].message.content},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print(f"Groq API error: {str(e)}")
            return Response(
                {"reply": "Something went wrong. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "message": "User registered successfully.",
            "token": token.key
        }, status=status.HTTP_201_CREATED)