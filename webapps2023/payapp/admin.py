from django.contrib import admin
from .models import AllTransactions, AccountBal, Notifications, OriginalSender

admin.site.register(AccountBal)
admin.site.register(AllTransactions)
admin.site.register(Notifications)
admin.site.register(OriginalSender)