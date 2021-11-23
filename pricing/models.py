from django.db import models
from django.contrib.auth import get_user_model

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


class Order(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.user.email}"
