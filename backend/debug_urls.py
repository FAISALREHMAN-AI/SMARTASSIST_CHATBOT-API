import os
import django
import sys

# Django settings ko locate karne ke liye env set karein
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

try:
    django.setup()
except Exception as e:
    print(f"\n❌ Django Setup Error: {e}")
    print("Tip: Make sure you are running this inside the 'backend' folder where 'manage.py' is located.")
    sys.exit(1)

from django.urls import get_resolver
from django.conf import settings
import importlib

print("\n🔍 ================== SMARTASSIST API URL DEBUGGER ==================")
print(f"✅ Django Version: {django.get_version()}")
print(f"⚙️  Settings Module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
print(f"📁 Root URLConf Configured: {settings.ROOT_URLCONF}")

try:
    urlconf_module = importlib.import_module(settings.ROOT_URLCONF)
    # Exact file path print karein jo Django use kar raha hai
    print(f"📍 ACTUAL URLS.PY FILE PATH BEING READ:\n   👉 {urlconf_module.__file__}")
    
    print("\n🌐 REGISTERED URL PATTERNS IN REAL-TIME:")
    resolver = get_resolver()
    patterns = resolver.url_patterns
    if not patterns:
        print(" ⚠️  No URL patterns registered!")
    for pattern in patterns:
        print(f"  - {pattern}")
        
except Exception as e:
    print(f"❌ Error while loading URLConf: {e}")
print("=====================================================================\n")