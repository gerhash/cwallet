from datetime import datetime
import random
from django.db.models import Q
from django.http import HttpResponse
from .forms import RegisterForm,DocumentUpdateForm,SendCoinForm,BuyCoinForm,WithDrawForm
from django.contrib.auth import login,logout,authenticate
from .models import Coin
from .score_logic import *
from .models import Transaction,Withdraw_requests,Calendar_record
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages  # For displaying error messages
from . import crea_records

def gen(request):
    if request.method == "GET":
        crea_records.record_gen()
        return HttpResponse("GENERATI")

@login_required(login_url='/login')
def home(request):
    coin = Coin.objects.first()
    transactions_raw = Transaction.objects.filter(
        Q(sender=request.user.username) | Q(receiver=request.user.username)
    )
    transactions = reversed(transactions_raw)
    money_balance = 0

    # Controllo se l'utente è autenticato
    if request.user.is_authenticated:
        user = request.user  # Ottieni l'istanza dell'utente autenticato
        user.balance = round(user.balance, 2)
        money_balance = round(user.balance * coin.value, 2)
        user.save()
    else:
        user = None  # Imposta user a None se l'utente non è autenticato

    # Recupera i dati per il grafico
    records = Calendar_record.objects.order_by('date')
    dates = [record.date.strftime('%Y-%m-%d') for record in records]
    values = [record.value for record in records]

    context = {
        'user': user,
        'coin': coin,
        'bal': round(money_balance, 2),
        'transactions': transactions,
        'dates': dates,
        'values': values
    }
    print(context)

    return render(request, "home.html", context)


@login_required(login_url='/login')
def verify_doc(request):
    if request.method == 'POST':
        document_form = DocumentUpdateForm(request.POST, request.FILES,instance=request.user)
        if document_form.is_valid():
            document_form.save()
            return redirect('home')  # Reindirizza alla pagina del profilo dopo l'aggiornamento
    else:
        document_form = DocumentUpdateForm(instance=request.user)
    return render(request, 'registration/doc_verify.html', {'form': document_form})



@login_required(login_url='/login')
def send_coin(request):
    coin = Coin.objects.first()  # Assuming you have only one coin
    bal = round(request.user.balance * coin.value,2)
    if request.method == 'POST':
        form = SendCoinForm(request.POST)
        if form.is_valid():
            user_balance = request.user.balance  # Access user balance
            value = form.cleaned_data['value']
            receiver_username = form.cleaned_data['receiver']

            if user_balance < value:
                messages.error(request, f"Insufficient balance. Your current balance is {user_balance:.2f}.")
            else:
                try:
                    receiver = CustomUser.objects.get(username=receiver_username)
                    if receiver.username == request.user.username:
                        messages.error(request,f"Your username can't be used!")
                        return render(request, 'actions/send.html',
                                      {'form': form, 'user_balance': request.user.balance,'bal':bal,'coin':coin})

                except CustomUser.DoesNotExist:
                    messages.error(request, f"Invalid receiver username. Please enter a valid username.")
                    return render(request, 'actions/send.html', {'form': form, 'user_balance': request.user.balance,'bal':bal,'coin':coin})

                current_datetime = datetime.datetime.now()  # Get current date and time in UTC
                formatted_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

                tov = round(value * coin.value)

                transazione = Transaction.objects.create(
                    type='IR',
                    value=form.cleaned_data['value'],
                    sender=request.user.username,
                    receiver=form.cleaned_data['receiver'],
                    tov=tov,
                    date=formatted_date
                )
                sendmoney(user_sender=request.user, user_receiver=form.cleaned_data['receiver'], value=value)
                return redirect('/home')  # Redirect on successful transaction
    else:
        form = SendCoinForm()

    return render(request, 'actions/send.html', {'form': form,'user_balance':request.user.balance,'bal':bal,'coin':coin})

@login_required(login_url='/login')
def receive(request):
    return render(request, 'actions/receive.html', {'user':request.user})


@login_required(login_url='/login')
def withdraw(request):
    coin = Coin.objects.first()
    bal = round(request.user.balance * coin.value,2)
    if request.method == 'POST':
            form = WithDrawForm(request.POST)
            if form.is_valid():
                value = form.cleaned_data['quantity_req']
                tov = round(value * coin.value,2)
                current_datetime = datetime.datetime.now()  # Get current date and time in UTC
                formatted_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                transazione = Transaction.objects.create(
                            type='CASHOUT',
                            value=value,
                            sender=f'{COIN_NAME}',
                            receiver=request.user.username,
                            tov=tov,
                            date=formatted_date
                        )
                record = Withdraw_requests.objects.create(
                    quantity_req=value,
                    iban=form.cleaned_data['iban'],
                    user=request.user.username,
                    date=formatted_date )

                cashout(user=request.user,value=value)

                return redirect('/home')  # Redirect on successful transaction
            else:
                messages.error(request, f"Transaction Not Completed, Error.")
                return render(request, 'actions/withdraw.html', {'form': form, 'user': request.user, 'coin': coin,'bal':bal})
    else:
        form = WithDrawForm()
    if request.user.is_docverified:
        return render(request, 'actions/withdraw.html', {'form': form, 'user': request.user, 'coin': coin,'bal':bal})
    else:
        return redirect('/verify-docs')

@login_required(login_url='/login')
def buy_coin(request):
    coin = Coin.objects.first()  # Assuming you have only one coin
    if request.method == 'POST':
        form = BuyCoinForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['value']
            tov = round(value * coin.value,2)
            current_datetime = datetime.datetime.now()  # Get current date and time in UTC
            formatted_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            code = form.cleaned_data['code']
            code_bonus = checkBonus(code)
            total = round(value + code_bonus,2)
            isCompleted = buyCoins(request.user,total)
            if isCompleted == True:
                transazione = Transaction.objects.create(
                        type='BUY',
                        value=form.cleaned_data['value'],
                        sender=f'{COIN_NAME}',
                        receiver=request.user.username,
                        tov=tov,
                        date=formatted_date
                    )
                if code_bonus > 0:
                    bonus = Transaction.objects.create(
                        type='BONUS',
                        value=code_bonus,
                        sender=f'{COIN_NAME}',
                        receiver=request.user.username,
                        tov=tov,
                        date=formatted_date
                    )

                return redirect('/home')  # Redirect on successful transaction
            else:
                messages.error(request, f"Transaction Not Completed, Error.")
                return render(request, 'actions/buy.html', {'form': form, 'user': request.user, 'coin': coin})
    else:
        form = BuyCoinForm()

    return render(request, 'actions/buy.html', {'form': form,'user':request.user,'coin':coin})


@login_required(login_url='/login')
def account(request):
    coin = Coin.objects.first()
    bal = round(request.user.balance * coin.value,2)
    return render(request,'account/account.html', {'user':request.user, 'bal':bal,'coin':coin})




def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            login(request,user)
            invite_score(user,ENTRYBONUS)
            return redirect('/home')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {"form":form})



