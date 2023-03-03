from django.db import models
from django.db.models import Q
from django.db.models import UniqueConstraint
from django.conf import settings


class Plan(models.Model):
    months = models.PositiveSmallIntegerField()
    default = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    saving = models.DecimalField(max_digits=6, decimal_places=2)
    stripe_product_id = models.CharField(max_length=32, blank=True, null=True)
    

    def __str__(self):
        return f"{self.months} months"

    class Meta:
        ordering = ('months', 'price')
        constraints = [
            UniqueConstraint(fields=['default'], condition=Q(default=True), name='unique_default_field'),
            UniqueConstraint(fields=['months'], name='unique_months_field')
            ]


class Order(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created} - {self.user.email}"
