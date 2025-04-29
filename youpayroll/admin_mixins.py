from django.contrib import admin
from payees.models import Payee


class PayeeRestrictAdmin(admin.ModelAdmin):
    """
    Base admin class that restricts data to the logged-in user's employee
    unless the user is a superuser.
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            payee = Payee.objects.get(user=request.user)
            return qs.filter(payee=payee)
        except Payee.DoesNotExist:
            return qs.none()

    def save_model(self, request, obj, form, change):
        if not obj.payee_id:
            try:
                obj.payee = Payee.objects.get(user=request.user)
            except Payee.DoesNotExist:
                pass
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields.pop('payee', None)
        return form
