import os
import sys
import django
import warnings
import pytest

# Add the src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_core.settings')
django.setup()

warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydantic") 