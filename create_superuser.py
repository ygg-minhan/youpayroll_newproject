import os
import django
import sys

# Dynamic path addition
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "youpayroll.settings.base")
django.setup()

from django.contrib.auth.models import User

def create_initial_superuser():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser 'admin' created.")
    else:
        print("Superuser 'admin' already exists.")

if __name__ == "__main__":
    create_initial_superuser()
