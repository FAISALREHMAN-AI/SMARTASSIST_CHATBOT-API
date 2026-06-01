from django.shortcuts import render

# Create your views here.
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google import genai
from dotenv import load_dotenv
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

load_dotenv()

# Gemini Client Initialize
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class SmartAssistChatView(APIView):
    
    # Swagger documentation ke liye schema definition
    @swagger_auto_schema(
        operation_description="Send a message to SmartAssist API powered by Gemini",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['message'],
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description="User's query")
            },
        ),
        responses={200: "Success Response", 400: "Bad Request"}
    )
    def post(self, request):
        user_message = request.data.get("message")
        
        if not user_message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Gemini model calling
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_message,
            )
            return Response({"reply": response.text}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)