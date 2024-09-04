import logging

from django.contrib import admin

from .models import Payment, PayRecordRegister, PayRun
from payees.utils import restrict_queryset_by_group


logger = logging.getLogger(__name__)


# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display = ["payee", "label"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return restrict_queryset_by_group(qs, request.user,
                                          payee_field='payee')


class PayRunAdmin(admin.ModelAdmin):
    list_display = ('month', 'year', 'status', 'created_by')
    list_filter = ('status', 'month', 'year')
    search_fields = ('status', 'month', 'year')
    readonly_fields = ('status', 'created_at')
    ordering = ['-created_at']


admin.site.register(Payment, PaymentAdmin)
admin.site.register(PayRecordRegister)
admin.site.register(PayRun, PayRunAdmin)
