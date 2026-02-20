from django.db import models
from auditlog.registry import auditlog
from payees.models import Payee

class PayRun(models.Model):
    run_date = models.DateField()
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[('DRAFT', 'Draft'), ('COMPLETED', 'Completed')], default='DRAFT')

    def __str__(self):
        return f"Pay Run {self.run_date}"

class Payment(models.Model):
    payee = models.ForeignKey(Payee, on_delete=models.CASCADE, related_name='payments')
    pay_run = models.ForeignKey(PayRun, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    reference_number = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Payment of {self.amount} to {self.payee.name}"

class PayRecordRegister(models.Model):
    pay_run = models.ForeignKey(PayRun, on_delete=models.CASCADE, related_name='registers')
    generated_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='payroll/registers/', null=True, blank=True)

    def __str__(self):
        return f"Register for {self.pay_run}"

class Form16(models.Model):
    payee = models.ForeignKey(Payee, on_delete=models.CASCADE, related_name='form16s')
    financial_year = models.CharField(max_length=20) # e.g. "2023-24"
    file = models.FileField(upload_to='payroll/form16s/', null=True, blank=True)

    def __str__(self):
        return f"Form16 - {self.payee.name} - {self.financial_year}"

class Form16Entry(models.Model):
    form16 = models.ForeignKey(Form16, on_delete=models.CASCADE, related_name='entries')
    section = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "Form16 entry"
        verbose_name_plural = "Form16 entries"

    def __str__(self):
        return f"{self.section} - {self.amount}"

auditlog.register(PayRun)
auditlog.register(Payment)
auditlog.register(PayRecordRegister)
auditlog.register(Form16)
auditlog.register(Form16Entry)
