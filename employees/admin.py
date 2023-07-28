from django.contrib import admin
from .models import Employee
from zohopeople.utils import get_employees_details


# Admin action to fetch employee details from zoho people
@admin.action(description="Fetch Employee details from Zoho people")
def fetch_details(modeladmin, request, queryset):
    for employee in queryset:
        emp_id = employee.emp_id
        # Calling the function get_employee_details and return response
        response_data = get_employees_details(emp_id).json()
        response_data_list = response_data["response"]["result"][0]
        for i in response_data_list.values():
            fetched_data = i[0]
            employee.name = fetched_data["FirstName"] + " " + fetched_data[
                "LastName"]
            employee.email = fetched_data["EmailID"]
            employee.pan_no = fetched_data["Pan_Number"]
            employee.address = fetched_data["Permanent_Address"]
            employee.save()


class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = ["name", "email", "pan_no", "address"]
    actions = [fetch_details]


admin.site.register(Employee, EmployeeAdmin)
