import os
import django
import sys

# Dynamic path addition to allow running from any directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youpayroll.settings.base')
django.setup()

from core.models import WikiCategory
from django.utils.text import slugify

def seed_wiki_categories():
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

if __name__ == "__main__":
    seed_wiki_categories()
