from django.shortcuts import get_object_or_404
from employees.models import Payee
from employees.constants import RESTRICTED_GROUPS


def restrict_queryset_by_group(qs, user, payee_field=None):
    # Restrict access for users if they are in RESTRICTED_GROUPS
    if user.groups.filter(name__in=RESTRICTED_GROUPS).exists():
        if payee_field:
            payee = get_object_or_404(Payee, user=user)
            qs = qs.filter(payee=payee)
        else:
            qs = qs.filter(user=user)
    return qs
