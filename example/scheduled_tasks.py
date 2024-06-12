import datetime
import time
import random
from .models import Coin
def coin_value():
    # Define the number of times to perform the action
    num_actions_per_day = 6

    # Calculate the interval between each action in seconds
    interval_seconds = 24 * 60 * 60 / num_actions_per_day

    # Main loop to perform the action
    while True:
        # Perform the action
        luckyValue()
        # Wait until the next interval
        time.sleep(interval_seconds)

#0 vuol dire +, 1 vuol dire -
def luckyValue():
    lucky = random.randint(0, 1)
    coin = Coin.objects.first()
    value = coin.value * 0.02 #percentuale aumento/decremento
    if lucky == 0:
        coin.value += value
    elif lucky == 1:
        coin.value -= value
    else:
        pass

    coin.value = round(coin.value,1)
    coin.save()


