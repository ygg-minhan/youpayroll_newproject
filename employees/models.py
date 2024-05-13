import uuid
from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog


# Create your models here.

# Model containing Tax Deducted at Source information
class TDS(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ("technical-consultants", "Technical Consultants"),
        ("professional-consultant", "Professional Consultant"),
        ("employment", "Employment"),
        ("apprentices", "Apprentices"),
    ]
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4,
                          editable=False)
    employment_type = models.CharField(max_length=50,
                                       choices=EMPLOYMENT_TYPE_CHOICES,
                                       unique=True)
    tds_percentage = models.FloatField()

    def __str__(self):
        return self.employment_type


auditlog.register(TDS)


# Stores the information of the Employee in the database
class Employee(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('terminated', 'Terminated'),
        ('resigned', 'Resigned')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='active')
    emp_id = models.UUIDField(primary_key=True, unique=True,
                              default=uuid.uuid4,
                          editable=False)
    emp_code = models.CharField(
        max_length=100, help_text="Employee ID obtained from Zoho people")
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    pan_no = models.CharField(max_length=10, null=True, blank=True)
    date_of_joining = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    employment_type = models.ForeignKey(TDS, on_delete=models.SET_NULL,
                                        blank=True, null=True,
                                        to_field="employment_type")

    def __str__(self):
        if self.full_name is not None:
            return self.full_name
        return str(self.emp_id)

    def delete(self, *args, **kwargs):
        self.status = 'terminated'
        self.save()


auditlog.register(Employee)


class Earning(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4,
                          editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    label = models.CharField(max_length=50)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.label


auditlog.register(Earning)


class BankDetails(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4,
                          editable=False)
    ACKNOWLEDGEMENT_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("disapproved", "Disapproved")
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    account_no = models.CharField(max_length=100, null=True, blank=True)
    account_holder_name = models.CharField(max_length=100, null=True,
                                           blank=True)
    account_type = models.CharField(max_length=10, null=True, blank=True)
    ifsc_code = models.CharField(max_length=100, null=True, blank=True)
    micr_code = models.CharField(max_length=100, null=True, blank=True)
    swift_code = models.CharField(max_length=100, null=True, blank=True)
    branch_address = models.TextField(null=True, blank=True)
    employee_acknowledgement = models.CharField(max_length=50,
                                                choices=ACKNOWLEDGEMENT_CHOICES,
                                                default="pending",
                                                unique=True)

    def __str__(self):
        return self.account_holder_name


auditlog.register(BankDetails)
