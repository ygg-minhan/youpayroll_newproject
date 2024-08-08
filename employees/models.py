import uuid
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog
from employees.upload_helpers import user_directory_path, validate_image
from employees.constants import (MONTH_CHOICES, TDS_LEGAL_NAME_CHOICES,
                                 STATUS_CHOICES, PAYEE_STATUS_HELP_TEXT)


# Create your models here.

# Model containing Tax Deducted at Source information
class TDS(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    tds_legal_name = models.CharField(max_length=50,
                                      choices=TDS_LEGAL_NAME_CHOICES,
                                      unique=True)
    tds_percentage = models.FloatField()

    class Meta:
        verbose_name = _("Tax Deducted at Source")
        verbose_name_plural = _("Tax Deducted at Source")

    def __str__(self):
        return self.tds_legal_name


auditlog.register(TDS)


# Stores the information of the Payee in the database
class Payee(models.Model):
    is_deleted = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='active',
                              help_text=PAYEE_STATUS_HELP_TEXT)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    hrm_id = models.CharField(max_length=10, help_text="Payee ID obtained "
                                                       "from Zoho people")
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    tds_type = models.ForeignKey(TDS, on_delete=models.SET_NULL, blank=True,
                                 null=True, to_field="tds_legal_name")
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    pan_no = models.CharField(max_length=10, null=True, blank=True)
    date_of_joining = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _("Payee")
        verbose_name_plural = _("Payees")

    def __str__(self):
        if self.full_name is not None:
            return self.full_name
        return self.hrm_id

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


auditlog.register(Payee)


class Payment(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    label = models.CharField(max_length=50)
    payee = models.ForeignKey(Payee, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        return self.label


auditlog.register(Payment)


class BankDetails(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    payee = models.ForeignKey(Payee, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    account_no = models.CharField(max_length=100, null=True, blank=True)
    account_holder_name = models.CharField(max_length=100, null=True,
                                           blank=True)
    account_type = models.CharField(max_length=10, null=True, blank=True)
    ifsc_code = models.CharField(max_length=100, null=True, blank=True)
    micr_code = models.CharField(max_length=100, null=True, blank=True)
    swift_code = models.CharField(max_length=100, null=True, blank=True)
    branch_address = models.TextField(null=True, blank=True)
    payee_acknowledgement = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name = _("Bank Detail")
        verbose_name_plural = _("Bank Details")

    def __str__(self):
        return self.account_holder_name

    def save(self, *args, **kwargs):
        if self.pk:
            current_instance = BankDetails.objects.get(pk=self.pk)
            if (self.payee != current_instance.payee or
                self.bank_name != current_instance.bank_name or
                self.account_no != current_instance.account_no or
                self.account_holder_name !=
                    current_instance.account_holder_name or
                self.account_type != current_instance.account_type or
                self.ifsc_code != current_instance.ifsc_code or
                self.micr_code != current_instance.micr_code or
                self.swift_code != current_instance.swift_code or
                    self.branch_address !=
                    current_instance.branch_address):
                self.payee_acknowledgement = False
        super().save(*args, **kwargs)


auditlog.register(BankDetails)


# Stores the details of amount paid to each tds type and their account details
class PayRecordRegister(models.Model):
    record_created = models.DateTimeField(auto_now_add=True)
    month = models.IntegerField(choices=MONTH_CHOICES)
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
        unique_together = ('payee', 'month')
        verbose_name = _("Pay Record Register")
        verbose_name_plural = _("Pay Record Registers")

    def __str__(self):
        if self.payee.full_name is not None:
            return self.payee.full_name
        return self.payee.hrm_id


auditlog.register(PayRecordRegister)


class PayRecord(models.Model):
    record_created = models.DateTimeField(auto_now_add=True)
    payee = models.ForeignKey(Payee, on_delete=models.CASCADE)
    month = models.IntegerField(choices=MONTH_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                                 blank=True)
    bank_account = models.CharField(null=True, blank=True, max_length=16)
    pay_register = models.ForeignKey(PayRecordRegister,
                                     on_delete=models.CASCADE)

    class Meta:
        unique_together = ('payee', 'month')
        verbose_name = _("Pay Record")
        verbose_name_plural = _("Pay Records")

    def __str__(self):
        if self.payee.full_name is not None:
            return self.payee.full_name
        return self.payee.hrm_id


auditlog.register(PayRecord)


# Stores the bank-acknowledgement file uploaded by the payee
class BankDetailsAck(models.Model):
    payee = models.ForeignKey(Payee, on_delete=models.CASCADE,
                              related_name='bank_acknowledgement')
    uploaded_date = models.DateTimeField(auto_now_add=True)
    bank_details_screenshot = models.ImageField(
        upload_to=user_directory_path, validators=[validate_image,
                                                   FileExtensionValidator(
                                                       allowed_extensions=[
                                                           'jpg', 'jpeg',
                                                           'png'])])
    # Indicates the approval status of the bank details. True if the bank
    # details are approved, False if rejected.
    is_approved = models.BooleanField(default=False)
    correction_comments = models.TextField(blank=True, null=True,
                                           help_text="Please specify any "
                                                     "mistaken areas found "
                                                     "in the bank details.")

    class Meta:
        verbose_name = _("Bank Detail Acknowledgement")
        verbose_name_plural = _("Bank Detail Acknowledgements")

    def __str__(self):
        return self.payee.hrm_id


auditlog.register(BankDetailsAck)


class PayRunStatusChoices(models.TextChoices):
    DUE = 'due', _('pay record entry creation in due')
    IN_PROGRESS = 'in_progress', _('pay record entry creation in progress')
    COMPLETED = 'completed',_('pay record entry creation completed')


class PayRun(models.Model):
    """
    This model keeps track of payment details for each month before
    processing payments.
    Payments are only made to payees who are active and have
    acknowledged their bank details.
    """
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField()
    status = models.CharField(max_length=20,
                              choices=PayRunStatusChoices.choices,
                              default=PayRunStatusChoices.DUE)

    class Meta:
        unique_together = ('month', 'year')
        verbose_name = _("Pay Run")
        verbose_name_plural = _("Pay Runs")

    def __str__(self):
        return (f"{self.get_month_display()} {self.year} - "
                f"{self.get_status_display()}")


auditlog.register(PayRun)
