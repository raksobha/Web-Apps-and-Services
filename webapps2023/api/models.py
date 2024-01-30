from django.db import models


class CurrencyConversion(models.Model):
    currency = {("GBP", "GBP"), ("USD", "USD"), ("EUR", "EUR")}
    start_currency = models.CharField(max_length=3, choices=currency)
    target_currency = models.CharField(max_length=3, choices=currency)
    conversion_rate = models.DecimalField(max_digits=8, decimal_places=4)

    def __str__(self):
        return f"{self.start_currency},{self.target_currency},{self.conversion_rate}"

