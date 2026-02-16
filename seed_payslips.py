import os
import django
import sys
from decimal import Decimal

# Add project root to path
sys.path.append('/Users/anshik/youpayroll_newproject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youpayroll_newproject.settings')
django.setup()

from core.models import Payslip
from django.contrib.auth.models import User

# List of months to seed
months = ["April", "May", "June", "July", "August", "September", "October", "November", "December", "January", "February", "March"]

def seed_payslips():
    for user in User.objects.all():
        # Seed for multiple financial years from 2020 to 2029
        for start_year in range(2020, 2030):
            for i, month in enumerate(months):
                year = start_year if i < 9 else start_year + 1
                
                # Generate realistic data
                gross = Decimal("82000.00")
                reimbursement = Decimal("10000.00")
                deductions = Decimal("1000.00")
                take_home = gross + reimbursement - deductions
                
                Payslip.objects.get_or_create(
                    user=user,
                    month=month,
                    year=year,
                    defaults={
                        'gross_pay': gross,
                        'reimbursement': reimbursement,
                        'deductions': deductions,
                        'take_home': take_home,
                        'file': 'payslips/mock_payslip.pdf',
                        'tax_worksheet': 'tax_worksheets/mock_worksheet.pdf'
                    }
                )
    print("Payslips seeded successfully for all users across 2020-2030!")

if __name__ == "__main__":
    seed_payslips()
