import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youpayroll_newproject.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Payslip
from django.core.files.base import ContentFile

def create_sample_payslip():
    try:
        user = User.objects.get(username='minhan')
        
        # Create a dummy PDF content
        dummy_content = b"%PDF-1.4\n1 0 obj < < /Type /Catalog /Pages 2 0 R > > endobj 2 0 obj < < /Type /Pages /Kids [3 0 R] /Count 1 > > endobj 3 0 obj < < /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R > > endobj 4 0 obj < < /Length 44 > > stream\nBT /F1 24 Tf 100 700 Td (Sample Payslip) Tj ET\nendstream\n"
        
        payslip_file = ContentFile(dummy_content, name="payslip_march.pdf")
        worksheet_file = ContentFile(dummy_content, name="tax_worksheet_march.pdf")

        # Create the Payslip record
        payslip, created = Payslip.objects.get_or_create(
            user=user,
            month='March',
            year=2024,
            defaults={
                'gross_pay': 2602.0,
                'reimbursement': 1602.0,
                'deductions': 0.0,
                'take_home': 80.0,
            }
        )
        
        payslip.file.save('payslip_march.pdf', payslip_file)
        payslip.tax_worksheet.save('tax_worksheet_march.pdf', worksheet_file)
        payslip.save()

        print(f"Successfully created/updated payslip for {user.username}")
    except User.DoesNotExist:
        print("User 'minhan' not found. Please check user list.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_sample_payslip()
