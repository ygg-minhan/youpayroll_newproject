from django.db import models
from auditlog.registry import auditlog

class Component(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class TaxDeductedAtSource(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Tax Deducted at Source"
        verbose_name_plural = "Tax Deducted at Source"

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"

auditlog.register(Component)
auditlog.register(TaxDeductedAtSource)
