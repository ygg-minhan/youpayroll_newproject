import logging
from django.contrib import admin
from django.contrib import messages
from .models import Employee, TDS, Wage, BankDetails
from zohopeople.utils import get_employees_details

logger = logging.getLogger(__name__)


# Admin action to fetch employee details from zoho people
@admin.action(description="Fetch Employee details from Zoho people")
def fetch_details(modeladmin, request, queryset):
    for employee in queryset:
        emp_id = employee.emp_id
        # Calling the function get_employee_details and return response
        try:
            response_data = get_employees_details(emp_id).json()
            response_data_list = response_data["response"]["result"][0]
        except Exception as e:
            logger.warning(e)
            response_data_list = {}

        if response_data_list:
            for i in response_data_list.values():
                fetched_data = i[0]
                employee.full_name = fetched_data["FirstName"] + \
                                     " " + fetched_data["LastName"]
                employee.email = fetched_data["EmailID"]
                employee.pan_no = fetched_data["Pan_Number"]
                employee.address = fetched_data["Permanent_Address"]
                employee.date_of_joining = fetched_data["Dateofjoining"]
                employee.save()
                messages.success(request, "Employee details were "
                                          "successfully fetched.")


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["emp_id", "full_name", "employment_type"]
    readonly_fields = ["full_name", "email", "pan_no", "address",
                       "date_of_joining"]
    actions = [fetch_details]


class BankDetailsAdmin(admin.ModelAdmin):
    list_display = ["employee", "bank_name", "account_type",
                    "employee_acknowledgement"]


admin.site.register(TDS)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Wage)
admin.site.register(BankDetails, BankDetailsAdmin)
