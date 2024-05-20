import uuid
from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog


# Create your models here.

# Model containing Tax Deducted at Source information
class TDS(models.Model):
    JOB_CATEGORY_CHOICES = [
        ("technical-consultants", "Technical Consultants"),
        ("professional-consultant", "Professional Consultant"),
        ("employment", "Employment"),
        ("apprentices", "Apprentices"),
    ]
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4,
                          editable=False)
    job_category = models.CharField(max_length=50,
                                       choices=JOB_CATEGORY_CHOICES,
                                       unique=True)
    tds_percentage = models.FloatField()

    def __str__(self):
        return self.job_category


auditlog.register(TDS)


# Stores the information of the Payee in the database
class Payee(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('terminated', 'Terminated'),
        ('resigned', 'Resigned')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='active')
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False,
                            primary_key=False)
    hrm_id = models.CharField(max_length=10, primary_key=True,
                              help_text="Payee ID obtained from Zoho people")
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    pan_no = models.CharField(max_length=10, null=True, blank=True)
    date_of_joining = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    tds_type = models.ForeignKey(TDS, on_delete=models.SET_NULL,
                                        blank=True, null=True,
                                        to_field="job_category")

    def __str__(self):
        if self.full_name is not None:
            return self.full_name
        return self.hrm_id

    def delete(self, *args, **kwargs):
        self.status = 'terminated'
        self.save()


auditlog.register(Payee)


class Payment(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4,
                          editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    label = models.CharField(max_length=50)
    payee = models.ForeignKey(Payee, on_delete=models.CASCADE)

    def __str__(self):
        return self.label


auditlog.register(Payment)


class BankDetails(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4,
                          editable=False)
    ACKNOWLEDGEMENT_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("disapproved", "Disapproved")
    ]
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
    payee_acknowledgement = models.CharField(max_length=50,
                                                choices=ACKNOWLEDGEMENT_CHOICES,
                                                default="pending",
                                                unique=True)

    def __str__(self):
        return self.account_holder_name


auditlog.register(BankDetails)


# Stores the details of amount paid to each tds type and their account details
class PayRecordRegister(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                   null=True, blank=True)
    payee = models.ForeignKey(Payee, on_delete=models.CASCADE)
    month = models.CharField(null=True, blank=True, max_length=15)
    account_number = models.CharField(null=True, blank=True, max_length=16)
    tds_percentage = models.FloatField(null=True, blank=True)

    def __str__(self):
        if self.payee.full_name is not None:
            return self.payee.full_name
        return self.payee.hrm_id


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
