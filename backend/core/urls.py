from django.contrib import admin
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
