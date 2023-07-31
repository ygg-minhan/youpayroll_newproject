from django.db import models


# Create your models here.

# Stores the information of the Employee in the database
class Employee(models.Model):
    emp_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    pan_no = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.emp_id)
