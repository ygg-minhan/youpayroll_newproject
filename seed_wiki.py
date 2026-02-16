import os
import django
import sys

# Add project root to path
sys.path.append('/Users/anshik/youpayroll_newproject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youpayroll_newproject.settings')
django.setup()

from core.models import WikiCategory
from django.utils.text import slugify

categories = [
    "How-To Guides",
    "System Architecture",
    "Security Decisions",
    "Coding Standards",
    "Deployment Docs"
]

for cat_name in categories:
    WikiCategory.objects.get_or_create(
        name=cat_name,
        defaults={'slug': slugify(cat_name), 'description': f'Documentation for {cat_name}'}
    )

print("Wiki Categories seeded successfully!")
