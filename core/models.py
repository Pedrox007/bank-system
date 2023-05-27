from django.db import models


class Account(models.Model):
    class TypeChoices(models.TextChoices):
        DEFAULT = "default"
        BONUS = "bonus"
        SAVINGS = "savings"

    number = models.CharField("Number", max_length=10, unique=True)
    balance = models.DecimalField("Balance", decimal_places=2, max_digits=20)
    type = models.CharField("Type", max_length=20, choices=TypeChoices.choices, default=TypeChoices.DEFAULT)
    score = models.IntegerField("Score", null=True, blank=True, default=None)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
