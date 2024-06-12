import datetime
import pytz
from django.utils import timezone
from .models import CustomUser, Coin, Bonus_codes, Transaction

COIN_NAME = 'LUACOIN'
#VALORI COSTANTI in MONETA NORMALE( EUR DOLLARS GBP)
ENTRYBONUS = 10.00
DOCVERIFYB0NUS = 20.00

RANKINGS = [
    {"name":'Starter',"value":0},# 0 score
    {"name":'Iron',"value":3},
    {"name":'Bronze',"value":10},
    {"name":'Silver',"value":20},
    {"name":'Gold',"value":50},
    {"name":'Diamond',"value":100},
    {"name":'Platinum',"value":500},
    {"name": 'GOAT', "value": 1000},
]



TIME_ZONE = 'Europe/Rome'  # Replace with your desired time zone
USE_TZ = True
def invite_score(user, value):
    user_inserted = user
    coin = Coin.objects.first()
    try:
        bonus = round(value / coin.value,2)
        user_with_invite_code = CustomUser.objects.get(code=user.invite_code)
        user.balance += bonus
        user_with_invite_code.balance += bonus
        tov = round(bonus * coin.value,2)
        current_datetime = datetime.datetime.now()  # Get current date and time in UTC
        formatted_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        bonus = Transaction.objects.create(
                type='BONUS',
                value=bonus,
                sender=user_with_invite_code.username,
                receiver=user.username,
                tov=tov,
                date=formatted_date
                )
        user.save()  # Salva le modifiche al bilancio dell'utente inserito
        user_with_invite_code.save()
    except CustomUser.DoesNotExist:
        user_with_invite_code = None

def sendmoney(user_sender,user_receiver,value):
    coin = Coin.objects.first()
    user_receiver = CustomUser.objects.get(username=user_receiver)
    user_sender.balance -= value
    user_receiver.balance += value
    user_sender.save()
    user_receiver.save()

def buyCoins(user,value):
    coin = Coin.objects.first()
    #fai transazione, se completa ritorna True, Se errore ritorna False,
    is_done = True
    if is_done:
        user.balance += value
        user.save()
        return True
    else:
        return False

def checkBonus(code):
    try:
        code_obj = Bonus_codes.objects.get(code=code)
        if code_obj.is_valid():
            return code_obj.value
        else:
            return 0
    except Bonus_codes.DoesNotExist:
        print("Invalid bonus code entered.")
        return 0

def cashout(user,value):
    user.balance -= value
    user.save()










