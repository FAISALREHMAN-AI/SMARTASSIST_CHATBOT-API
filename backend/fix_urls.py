import os

# Naya, bilkul sahi urls.py ka content
urls_content = """from django.contrib import admin
from django.urls import path
from api.views import SmartAssistChatView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="SmartAssist API",
      default_version='v1',
      description="Advanced Full-Stack Chatbot API documentation",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chat/', SmartAssistChatView.as_view(), name='chat'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
"""

def main():
    print("\n🔧 ================== SMARTASSIST URL AUTO-PATCHER ==================")
    
    # Path verify karein jahan file likhni hai
    target_path = os.path.join("core", "urls.py")
    
    if not os.path.exists("manage.py"):
        print("❌ Error: Aap galat directory me hain! Is script ko 'backend' folder me manage.py ke sath hona chahiye.")
        return

    try:
        # File ko write karein (puraani empty ya basic file overwrite ho jayegi)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(urls_content)
        print(f"✅ SUCCESS! Sahi code successfully write ho gaya hai:")
        print(f"👉 Path: {os.path.abspath(target_path)}")
        
    except Exception as e:
        print(f"❌ Error writing urls.py: {e}")
    print("=====================================================================\n")

if __name__ == "__main__":
    main()