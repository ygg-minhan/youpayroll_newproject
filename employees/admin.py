import logging
from django.contrib import admin
from django.contrib import messages
from .models import (Payee, TDS, Payment, BankDetails, PayRecordRegister,
                     PayRecord, BankDetailsAck)
from employees.utils import restrict_queryset_by_group
from zohopeople.utils import get_employees_details


logger = logging.getLogger(__name__)


# Admin action to fetch payee details from zoho people
@admin.action(description="Fetch payee details from Zoho people")
def fetch_details(modeladmin, request, queryset):
    for payee in queryset:
        payee_id = payee.hrm_id
        # Calling the function get_employee_details and return response
        try:
            response_data = get_employees_details(payee_id).json()
            response_data_list = response_data["response"]["result"][0]
        except Exception as e:
            logger.warning(e)
            response_data_list = {}

        if response_data_list:
            for i in response_data_list.values():
                fetched_data = i[0]
                payee.full_name = fetched_data["FirstName"] + \
                                     " " + fetched_data["LastName"]
                payee.email = fetched_data["EmailID"]
                payee.pan_no = fetched_data["Pan_Number"]
                payee.address = fetched_data["Permanent_Address"]
                payee.date_of_joining = fetched_data["Dateofjoining"]
                payee.save()
                messages.success(request, "Payee details were "
                                          "successfully fetched.")


class PayeeAdmin(admin.ModelAdmin):
    list_display = ["hrm_id", "full_name", "tds_type", "status"]
    readonly_fields = ["full_name", "email", "pan_no", "address",
                       "date_of_joining"]
    ordering = ("status",)
    actions = [fetch_details]

    def delete_queryset(self, request, queryset):
        queryset.update(status='terminated', is_deleted=True)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return restrict_queryset_by_group(qs, request.user)


class BankDetailsAdmin(admin.ModelAdmin):
    list_display = ["payee", "bank_name", "account_type",
                    "payee_acknowledgement"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return restrict_queryset_by_group(qs, request.user,
                                          payee_field='payee')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ["payee", "label"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return restrict_queryset_by_group(qs, request.user,
                                          payee_field='payee')


class PayRecordAdmin(admin.ModelAdmin):
    list_display = ["payee", "month"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return restrict_queryset_by_group(qs, request.user,
                                          payee_field='payee')


admin.site.register(TDS)
admin.site.register(Payee, PayeeAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(BankDetails, BankDetailsAdmin)
admin.site.register(BankDetailsAck)
admin.site.register(PayRecordRegister)
admin.site.register(PayRecord, PayRecordAdmin)
