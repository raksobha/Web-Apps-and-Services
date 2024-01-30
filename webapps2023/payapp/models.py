from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import uuid


class AccountBal(models.Model):
    CURRENCY = [('GBP', 'GB Pounds'), ('USD', 'US dollars'), ('EUR', 'Euros')]
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, choices=CURRENCY, default='GBP')
    account_bal = models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name}, {self.currency}, {self.account_bal}"


class PayMoney(models.Model):
    dst_username = models.CharField(max_length=30)
    transfer_amount = models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return f"{self.dst_username}, {self.transfer_amount}"


class AllTransactions(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    exact_time_created = models.DateTimeField(default=timezone.now)
    TYPEOFTRANSACTION = [('sent', 'Sent'), ('received', 'Received'), ('requested', 'Requested')]
    type_of_transaction = models.CharField(max_length=9, choices=TYPEOFTRANSACTION)
    amount = models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(0.01)])
    other_user = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}, {self.date}, {self.exact_time_created} {self.type_of_transaction}, " \
               f"{self.amount}, {self.other_user}"


# Used to store an id so that original request is linked to the request sent to the other user
class OriginalSender(models.Model):
    id = models.CharField(primary_key=True, max_length=100, blank=True, unique=True, default=uuid.uuid4)

    def __str__(self):
        return f"{self.id}"


class Notifications(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    requester = models.CharField(max_length=100, blank=True, )
    TYPEOFTRANSACTION = [('requested', 'has requested a payment of'),
                         ('rejected', 'has rejected the requested payment of'),
                         ('paid', 'has paid the requested payment of'),
                         ('sent', 'You sent a payment of'),
                         ('request', 'You requested a payment of')]
    type_of_transaction = models.CharField(max_length=50, choices=TYPEOFTRANSACTION)
    time_of_notification = models.DateTimeField(default=timezone.now())
    seen = models.BooleanField(default=False)
    other_user = models.CharField(max_length=30)
    amount = models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return f"{self.name}, {self.type_of_transaction}, {self.time_of_notification}, {self.seen}, {self.other_user}, {self.amount}, {self.requester}"


