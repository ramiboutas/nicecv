from django.db import models


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
