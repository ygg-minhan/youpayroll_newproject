from django.shortcuts import get_object_or_404
from employees.models import Employee
from employees.constants import RESTRICTED_GROUPS


def restrict_queryset_by_group(qs, user, employee_field=None):
    # Restrict access for users if they are in RESTRICTED_GROUPS
    if user.groups.filter(name__in=RESTRICTED_GROUPS).exists():
        if employee_field:
            employee = get_object_or_404(Employee, user=user)
            qs = qs.filter(employee=employee)
        else:
            qs = qs.filter(user=user)
    return qs
