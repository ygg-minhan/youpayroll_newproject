from django.contrib import admin
from .models import Employee


# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = ["name", "email", "pan_no", "address"]


admin.site.register(Employee, EmployeeAdmin)
