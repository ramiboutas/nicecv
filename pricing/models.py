from django.db import models
from django.contrib.auth import get_user_model

class Plan(models.Model):
    months = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.months} months"


class Order(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.user.email}"
