import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youpayroll_newproject.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Document
from django.core.files.base import ContentFile

def seed_documents():
    try:
        user = User.objects.get(username='minhan')
        
        # Create a dummy PDF content
        dummy_content = b"%PDF-1.4\n1 0 obj < < /Type /Catalog /Pages 2 0 R > > endobj 2 0 obj < < /Type /Pages /Kids [3 0 R] /Count 1 > > endobj 3 0 obj < < /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R > > endobj 4 0 obj < < /Length 44 > > stream\nBT /F1 24 Tf 100 700 Td (Sample Document) Tj ET\nendstream\n"
        
        docs_to_create = [
            {'title': 'Form 16', 'description': 'Annual income tax form'},
            {'title': 'Salary Certificate', 'description': 'Current salary proof'},
            {'title': 'Investment Declaration', 'description': 'Tax saving proofs'}
        ]

        for doc_data in docs_to_create:
            doc, created = Document.objects.get_or_create(
                user=user,
                title=doc_data['title'],
                defaults={'description': doc_data['description'], 'status': 'PENDING'}
            )
            if not doc.file:
                sample_file = ContentFile(dummy_content, name=f"{doc_data['title'].lower().replace(' ', '_')}.pdf")
                doc.file.save(sample_file.name, sample_file)
                doc.save()
            print(f"Document '{doc.title}' ready for {user.username}")

    except User.DoesNotExist:
        print("User 'minhan' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    seed_documents()
