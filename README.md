
![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)


# CWallet

CWallet is the basic template for creating a user-controlled electronic exchange currency.
It consists of managing electronic money (not existing on blockchains) and allowing it to be exchanged, bought, received, withdrawn, earned using invitation codes.

The use is purely for research purposes,
this project was created by me to get familiar with DJANGO and MYSQL.
I assume no responsibility for improper use of this repository.

-----

The Ponzi scheme is a fraudulent economic sales model created by Charles Ponzi, which promises strong profits to the first investors, to the detriment of new "investors", who in turn are victims of the scam.
## Installation

At this moment it is only possible to use it locally as there is no configuration with PostgreSQL remotely.


## 1. Clone Repository

```javascript
git clone https://github.com/gerhash/wallet-django.git
```

## 2. Install Dependencies

```javascript
pip install -r requirements.txt
```

## 3. Run Server

```javascript
python manage.py runserver
```
## demo
## v0.1 Alpha

First version still under development, many functions to be implemented and the UI to be improved


#### Auth&Login

Login and Register page managed with django including encryption, when registering an invitation code is asked (optional), if entered a bonus is given to both users, both the invited person and the person who shared the code

#### Dashboard

At the top left there is a yellow box with the user's invitation code inside, by sharing it it will be possible to receive bonuses and rise in rank (to be implemented)

Subsequently there is a screen that includes the name of the coin and the actual balance of the user, both in euros (or chosen currency) and in the value of the coin

4 action buttons are present continuing below:
- Send: Allows you to send an amount of money to another user via your username
- Receive: Sharing your username you can receive coins
- Buy: You can purchase a desired amount of the coin, with the possibility of entering a bonus code
- Withdraw: Withdraw your money directly to an IBAN, but you need to verify the documents first

We now have a bread that contains transaction history.
They can be of 5 types, and they all contain quantity and date and time:

- Sent: Coin sent to user X 
- Received: Coin received from user X 
- Buy: Coin purchased
- Cashout: Coin Withdrawn
- Bonus: Coin Earned with bonus

Going down we have a dashboard that shows us the current value of the coin, with a graph (using Chart.js) that shows us its trend over time


#### Account

In this section we have the avatar image at the top with username and other personal information

If the document verification has not been carried out, there is a button that reminds us to do it.

We have the wallet with the user's balance and then a screen that reminds us of the price of the coin, the invitation code and the ranking statistics and the number of people invited by us.
In the future it will be implemented by ensuring that rewards are obtained based on rank and people invited
## 🛠 Skills
HTML, CSS, JavaScript, Python, Django, MySQL, Bootstrap

