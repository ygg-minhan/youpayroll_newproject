import uuid

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User

from auditlog.registry import auditlog

from .utils import get_month_name
from payees.models import Payee


# Create your models here.

class Payment(models.Model):
    """ Stores the information of the Payee salary details """

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    label = models.CharField(max_length=50)
    payee = models.OneToOneField(Payee, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        return self.label


auditlog.register(Payment)


class PayRunStatusChoices(models.TextChoices):
    DUE = 'due', _('DUE')
    IN_PROGRESS = 'in_progress', _('IN PROGRESS')
    COMPLETED = 'completed', _('COMPLETED')
    REJECTED = 'rejected', _('REJECTED')
    APPROVED = 'approved', _('APPROVED')


class PayRun(models.Model):
    """
    This model keeps track of payment details for each month before
    processing payments.
    Payments are only made to payees who are active and have
    acknowledged their bank details.
    """
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    month = models.IntegerField()
    year = models.IntegerField()
    status = models.CharField(max_length=20,
                              choices=PayRunStatusChoices.choices,
                              default=PayRunStatusChoices.DUE)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   editable=False, null=True, blank=True)

    class Meta:
        verbose_name = _("Pay Run")
        verbose_name_plural = _("Pay Runs")

    def display_month_name(self):
        return get_month_name(self.month)

    def __str__(self):
        return (f"{self.display_month_name()} {self.year} - "
                f"{self.get_status_display()}")


auditlog.register(PayRun)


class PayRecordRegister(models.Model):
    """ Stores the details of amount paid to each tds type and their account
    details after each successful Pay run """

    record_created = models.DateTimeField(auto_now_add=True)
    pay_run = models.ForeignKey(PayRun, on_delete=models.CASCADE, null=True,
                                blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                                 blank=True)
    payee = models.ForeignKey(Payee, on_delete=models.CASCADE)

    bank_name = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(null=True, blank=True, max_length=16)
    account_holder_name = models.CharField(max_length=100, null=True,
                                           blank=True)
    account_type = models.CharField(max_length=10, null=True, blank=True)
    ifsc_code = models.CharField(max_length=100, null=True, blank=True)
    micr_code = models.CharField(max_length=100, null=True, blank=True)
    swift_code = models.CharField(max_length=100, null=True, blank=True)
    branch_address = models.TextField(null=True, blank=True)
    tds_percentage = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('payee', 'pay_run')
        ordering = ['-record_created']
        verbose_name = _("Pay Record Register")
        verbose_name_plural = _("Pay Record Registers")

    def __str__(self):
        return (f"{self.payee} - {self.pay_run.month} / "
                f"{self.pay_run.year}  -  {self.pay_run.get_status_display()}")


auditlog.register(PayRecordRegister)
