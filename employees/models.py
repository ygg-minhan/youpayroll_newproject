import uuid
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog
from employees.upload_helpers import user_directory_path, validate_image
from employees.constants import MONTH_CHOICES


# Create your models here.

# Model containing Tax Deducted at Source information
class TDS(models.Model):
    TDS_LEGAL_NAME_CHOICES = [
        ("technical-consultants", "Technical Consultants"),
        ("professional-consultant", "Professional Consultant"),
        ("employment", "Employment"),
        ("apprentices", "Apprentices"),
    ]
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    tds_legal_name = models.CharField(max_length=50,
                                      choices=TDS_LEGAL_NAME_CHOICES,
                                      unique=True)
    tds_percentage = models.FloatField()

    def __str__(self):
        return self.tds_legal_name


auditlog.register(TDS)


# Stores the information of the Payee in the database
class Payee(models.Model):
    is_deleted = models.BooleanField(default=False)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('terminated', 'Terminated'),
        ('resigned', 'Resigned')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='active')
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    hrm_id = models.CharField(max_length=10, help_text="Payee ID obtained "
                                                       "from Zoho people")
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    pan_no = models.CharField(max_length=10, null=True, blank=True)
    date_of_joining = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    tds_type = models.ForeignKey(TDS, on_delete=models.SET_NULL, blank=True,
                                 null=True, to_field="tds_legal_name")

    def __str__(self):
        if self.full_name is not None:
            return self.full_name
        return self.hrm_id

    def delete(self, *args, **kwargs):
        self.status = 'terminated'
        self.is_deleted = True
        self.save()


auditlog.register(Payee)


class Payment(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    label = models.CharField(max_length=50)
    payee = models.ForeignKey(Payee, on_delete=models.CASCADE)

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
    payee_acknowledgement = models.BooleanField(default=False)

    def __str__(self):
        return self.account_holder_name


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

    def __str__(self):
        if self.payee.full_name is not None:
            return self.payee.full_name
        return self.payee.hrm_id

    class Meta:
        unique_together = ('payee', 'month')


auditlog.register(PayRecordRegister)


class PayRecord(models.Model):
    payee = models.ForeignKey(Payee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                                 blank=True)
    month = models.CharField(null=True, blank=True, max_length=15)
    bank_account = models.CharField(null=True, blank=True, max_length=16)
    pay_register = models.ForeignKey(PayRecordRegister,
                                     on_delete=models.CASCADE)

    def __str__(self):
        if self.payee.full_name is not None:
            return self.payee.full_name
        return self.payee.hrm_id


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

    def __str__(self):
        return self.payee.hrm_id


auditlog.register(BankDetailsAck)
