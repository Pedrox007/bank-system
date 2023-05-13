from django.db import models


class Account(models.Model):
    number = models.CharField("Number", max_length=10, unique=True)
    balance = models.DecimalField("Balance", decimal_places=2, max_digits=20)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
