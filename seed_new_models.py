import os
import django
import random
import sys
from datetime import date, timedelta
from decimal import Decimal

sys.path.append('/Users/anshik/youpayroll_newproject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youpayroll.settings.base')
django.setup()

from django.contrib.auth.models import User
from configs.models import Component, TDS
from payees.models import Payee, BankDetails, BankDetailsAck
from payroll.models import PayRun, Payment, PayRecordRegister, Form16, Form16Entries

def seed():
    print("Seeding new models...")
    
    # Configs
    comp1, _ = Component.objects.get_or_create(component_name="Basic Pay", defaults={'operation': 'sum'})
    comp2, _ = Component.objects.get_or_create(component_name="HRA", defaults={'operation': 'sum'})
    comp3, _ = Component.objects.get_or_create(component_name="Special Allowance", defaults={'operation': 'sum'})
    
    tds1, _ = TDS.objects.get_or_create(tds_legal_name="Individual", defaults={'tds_percentage': 10.00})
    tds2, _ = TDS.objects.get_or_create(tds_legal_name="Company", defaults={'tds_percentage': 2.00})

    # Users / Payees
    users = User.objects.all()
    if not users:
        print("No users found. Create a user first.")
        # Create a test admin user if none exists
        admin_user, _ = User.objects.get_or_create(
            username='admin', 
            defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@example.com'}
        )
        admin_user.set_password('admin123')
        admin_user.save()
        users = [admin_user]

    for user in users:
        payee, created = Payee.objects.get_or_create(
            user=user,
            defaults={
                'full_name': user.get_full_name() or user.username, 
                'email': user.email,
                'hrm_id': f"HR{random.randint(1000, 9999)}",
                'tds_type': tds1
            }
        )
        
        # OneToOne Payment
        Payment.objects.get_or_create(
            payee=payee,
            defaults={'amount': Decimal("50000.00"), 'label': 'Monthly Salary'}
        )

        if created:
            bd = BankDetails.objects.get_or_create(
                payee=payee,
                defaults={
                    'account_no': f"73030100{random.randint(1000, 9999)}",
                    'bank_name': "ICICI Bank",
                    'account_holder_name': payee.full_name,
                    'ifsc_code': "ICIC0007",
                    'branch_address': "Infopark Kochi"
                }
            )
            BankDetailsAck.objects.get_or_create(
                payee=payee,
                defaults={'is_approved': True}
            )

    # Payroll
    today = date.today()
    for i in range(1, 4):
        run_date = today - timedelta(days=30 * i)
        pay_run, _ = PayRun.objects.get_or_create(
            month=run_date.month,
            year=run_date.year,
            defaults={'status': 'completed'}
        )
        
        for payee in Payee.objects.all():
            PayRecordRegister.objects.get_or_create(
                payee=payee,
                pay_run=pay_run,
                defaults={
                    'amount': Decimal(random.randint(50000, 150000)),
                    'bank_name': "ICICI Bank",
                    'account_number': f"73030100{random.randint(1000, 9999)}",
                    'account_holder_name': payee.full_name,
                    'ifsc_code': "ICIC0007",
                    'gross_amount': Decimal(random.randint(60000, 160000)),
                }
            )

    print("Success: New models seeded.")

if __name__ == "__main__":
    seed()
