from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from auditlog.registry import auditlog

class Payee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='payee', null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_payee(sender, instance, created, **kwargs):
    if created:
        Payee.objects.get_or_create(user=instance, defaults={'name': instance.username, 'email': instance.email})

@receiver(post_save, sender=User)
def save_payee(sender, instance, **kwargs):
    if hasattr(instance, 'payee'):
        instance.payee.save()

class BankDetail(models.Model):
    payee = models.ForeignKey(Payee, on_delete=models.CASCADE, related_name='bank_details')
    account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"

class BankDetailAcknowledgement(models.Model):
    bank_detail = models.OneToOneField(BankDetail, on_delete=models.CASCADE, related_name='acknowledgement')
    acknowledged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    acknowledged_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING')

    def __str__(self):
        return f"Acknowledgement for {self.bank_detail}"

auditlog.register(Payee)
auditlog.register(BankDetail)
auditlog.register(BankDetailAcknowledgement)
