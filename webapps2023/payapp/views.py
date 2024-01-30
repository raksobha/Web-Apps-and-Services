import decimal
import requests

from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from payapp.models import AllTransactions, AccountBal, Notifications, OriginalSender
from payapp.forms import PayForm, RequestForm
from django.db import transaction
from. import models


@csrf_protect
def home(request):
    if request.user.is_authenticated:
        return render(request, "main/home.html")
    else:
        return redirect("login")


@csrf_protect
def transactions(request):
    if request.user.is_authenticated:
        user_logged_in = User(request.user.id)
        past_transactions = AllTransactions.objects.filter(name=user_logged_in).order_by('-exact_time_created')
        account_bal = AccountBal.objects.filter(name=user_logged_in)[0]
        print(account_bal)
    else:
        return redirect("login")
    return render(request, "main/transactions.html", {"account_bal": account_bal, "past_transactions": past_transactions})


@csrf_protect
def notifications(request):
    user_logged_in = request.user.id
    old_notifications = Notifications.objects.filter(name=user_logged_in, seen=True).order_by('-time_of_notification')
    new_notifications = Notifications.objects.filter(name=user_logged_in, seen=False).order_by('-time_of_notification')
    account_bal = AccountBal.objects.filter(name=user_logged_in)[0]
    return render(request, "main/notifications.html", {"old_notifications": old_notifications, "new_notifications": new_notifications, "account_bal": account_bal})


@csrf_protect
def make_payment(request, notif_id):
    src_username = request.user.username
    src_bal = models.AccountBal.objects.select_related().get(name__username=src_username)

    if request.session.get('payment_successful', False):
        request.session['payment_successful'] = False
        return redirect(request.path)

    if request.method == 'POST':
        transaction_form = PayForm(request.POST)

        if transaction_form.is_valid():

            dst_username = transaction_form.cleaned_data["dst_username"]
            if dst_username == request.user.username:
                messages.error(request, "You can't make a payment to yourself")
            elif src_bal.account_bal < transaction_form.cleaned_data["transfer_amount"]:
                messages.error(request, "Insufficient Funds")
            else:
                try:
                    src_amount = transaction_form.cleaned_data["transfer_amount"]
                    dst_bal = AccountBal.objects.select_related().get(name__username=dst_username)
                    url = "https://127.0.0.1:8000/"
                    url = requests.get(url + f'conversion/{src_bal.currency}/{dst_bal.currency}', verify="C:/Users/ogarr/Documents/Web Applications and Services/webapps2023/127-0-0-1-chain.pem")
                    dst_amount = src_amount * decimal.Decimal(url.json()[0]['conversion_rate'])
                    with transaction.atomic():
                        src_bal.account_bal -= src_amount
                        src_bal.save()
                        dst_bal.account_bal += dst_amount
                        dst_bal.save()

                        user_payer = User(request.user.id)
                        date = timezone.now()
                        exact_date = timezone.now()
                        type_of_transaction = 'sent'

                        payer_transaction = AllTransactions(name=user_payer, date=date, type_of_transaction=type_of_transaction, amount=src_amount, other_user=dst_username)
                        payer_transaction.save()

                        type_of_transaction = 'received'
                        user_payee = models.User.objects.select_related().get(username=dst_username)
                        payee_transaction = AllTransactions(name=user_payee, date=date, type_of_transaction=type_of_transaction, amount=dst_amount, other_user=src_username)
                        payee_transaction.save()

                        request.session['payment_successful'] = True
                        messages.info(request, "Payment Successful")
                        return render(request, "main/home.html")
                except AccountBal.DoesNotExist:
                    messages.error(request, "Account holder does not exist")
        else:
            messages.error(request, f"Submitted form is invalid")
    else:
        if notif_id > 0:
            request_transaction = Notifications.objects.filter(id=notif_id)[0]
            request_transaction.seen = True
            request_transaction.save()
            transaction_form = PayForm(initial={"dst_username": request_transaction.other_user, "transfer_amount": request_transaction.amount})
        else:
            transaction_form = PayForm()
    return render(request, "main/makePayment.html", {"transaction_form": transaction_form})


@csrf_protect
def request_payment(request):
    if request.method == 'POST':
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            name = User(request.user.id)
            other_user = request_form.cleaned_data['other_user']
            if other_user == request.user.username:
                messages.error(request, "You can't request a payment from yourself")
            else:
                try:
                    with transaction.atomic():
                        receiver = models.User.objects.select_related().get(username=other_user)
                        type_of_transaction = "request"
                        amount = request_form.cleaned_data['amount']
                        sender = OriginalSender()
                        sender.save()
                        requester = sender.id
                        requester_name = request.user.username
                        request_notif = Notifications(name=name, requester=requester, time_of_notification=timezone.now(), type_of_transaction=type_of_transaction, other_user=other_user, amount=amount)
                        dst_account = AccountBal.objects.select_related().get(name__username=other_user)
                        src_username = request.user.username
                        src_account = models.AccountBal.objects.select_related().get(name__username=src_username)
                        url = "https://127.0.0.1:8000/"
                        url = requests.get(url + f'conversion/{src_account.currency}/{dst_account.currency}', verify="C:/Users/ogarr/Documents/Web Applications and Services/webapps2023/127-0-0-1-chain.pem")
                        dst_amount = amount * decimal.Decimal(url.json()[0]['conversion_rate'])
                        requested_notif = Notifications(name=receiver, requester=requester, time_of_notification=timezone.now(), type_of_transaction='requested', other_user=requester_name, amount=dst_amount)
                        request_notif.save()
                        requested_notif.save()
                        return redirect("notifications")
                except User.DoesNotExist:
                    messages.error(request, "Account holder does not exist")
        else:
            messages.error(request, "Submitted form is invalid")
    request_form = RequestForm()
    return render(request, "main/requestPayment.html", {"request_form": request_form})

@csrf_protect
def reject_payment(request, notif_id):
    notification = Notifications.objects.filter(id=notif_id)[0]
    notification.seen = True
    original_sender_id = notification.requester
    notification_original = Notifications.objects.filter(requester=original_sender_id)[0]

    rejected_notification = Notifications(name=notification_original.name, requester=original_sender_id, time_of_notification=timezone.now(), type_of_transaction="rejected", other_user=notification.name, amount=notification.amount)

    notification.save()
    rejected_notification.save()
    return redirect("notifications")

@csrf_protect
def seen_notification(request, notif_id):
    notification = Notifications.objects.filter(id=notif_id)[0]
    notification.seen = True
    notification.save()
    return redirect("notifications")
# @csrf_protect
# def requestPayment(request):
#
