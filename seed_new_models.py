import os
import django
import random
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youpayroll_newproject.settings')
django.setup()

from django.contrib.auth.models import User
from configs.models import Component, TaxDeductedAtSource
from payees.models import Payee, BankDetail, BankDetailAcknowledgement
from payroll.models import PayRun, Payment, PayRecordRegister, Form16, Form16Entry

def seed():
    print("Seeding new models...")
    
    # Configs
    comp1, _ = Component.objects.get_or_create(name="Basic Pay", description="Base salary component")
    comp2, _ = Component.objects.get_or_create(name="HRA", description="House Rent Allowance")
    comp3, _ = Component.objects.get_or_create(name="Special Allowance", description="Fixed special allowance")
    
    tds1, _ = TaxDeductedAtSource.objects.get_or_create(name="Income Tax", percentage=10.00)
    tds2, _ = TaxDeductedAtSource.objects.get_or_create(name="Professional Tax", percentage=2.00)

    # Users / Payees
    users = User.objects.all()
    if not users:
        print("No users found. Create a user first.")
        return

    for user in users:
        payee, created = Payee.objects.get_or_create(
            user=user,
            defaults={'name': user.get_full_name() or user.username, 'email': user.email}
        )
        if created:
            bd = BankDetail.objects.create(
                payee=payee,
                account_number=f"73030100{random.randint(1000, 9999)}",
                ifsc_code="ICIC0007",
                bank_name="ICICI Bank",
                branch_name="Infopark Kochi"
            )
            BankDetailAcknowledgement.objects.get_or_create(
                bank_detail=bd,
                defaults={'acknowledged_by': User.objects.filter(is_staff=True).first(), 'status': 'APPROVED'}
            )

    # Payroll
    today = date.today()
    for i in range(3):
        run_date = today - timedelta(days=30 * i)
        pay_run, _ = PayRun.objects.get_or_create(
            run_date=run_date,
            defaults={'description': f"Payroll for {run_date.strftime('%B %Y')}", 'status': 'COMPLETED'}
        )
        
        for payee in Payee.objects.all():
            Payment.objects.get_or_create(
                payee=payee,
                pay_run=pay_run,
                defaults={
                    'amount': random.randint(50000, 150000),
                    'payment_date': run_date + timedelta(days=5),
                    'reference_number': f"REF{random.randint(100000, 999999)}"
                }
            )
        
        PayRecordRegister.objects.get_or_create(pay_run=pay_run)

    for payee in Payee.objects.all():
        f16, _ = Form16.objects.get_or_create(
            payee=payee,
            financial_year="2023-24"
        )
        Form16Entry.objects.get_or_create(form16=f16, section="Salaries", defaults={'amount': 1200000})
        Form16Entry.objects.get_or_create(form16=f16, section="Deductions", defaults={'amount': 150000})

    print("Success: New models seeded.")

if __name__ == "__main__":
    seed()
