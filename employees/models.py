from django.db import models


# Create your models here.

# Model containing Tax Deducted at Source information
class TDS(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ("Technical consultants", "Technical consultants"),
        ("Professional Consultant", "Professional Consultant"),
        ("Employment", "Employment"),
        ("Intern", "Intern"),
    ]
    employment_type = models.CharField(max_length=50,
                                       choices=EMPLOYMENT_TYPE_CHOICES,
                                       unique=True)
    tds_percentage = models.IntegerField()

    def __str__(self):
        return self.employment_type


# Stores the information of the Employee in the database
class Employee(models.Model):
    emp_id = models.CharField(max_length=100, primary_key=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    pan_no = models.CharField(max_length=10, null=True, blank=True)
    date_of_joining = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    employment_type = models.ForeignKey(TDS, on_delete=models.SET_NULL,
                                        blank=True, null=True,
                                        to_field="employment_type")

    def __str__(self):
        return self.full_name


class Wage(models.Model):
    wage = models.FloatField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.full_name


class BankDetails(models.Model):
    ACKNOWLEDGEMENT_CHOICES = [
        ("Pending", "PENDING"),
        ("Confirmed", "CONFIRMED"),
        ("Disapproved", "DISAPPROVED")

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
                                                default="Pending",
                                                unique=True)

    def __str__(self):
        return self.employee.full_name
