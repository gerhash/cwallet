
![cwallet](https://github.com/gerhash/wallet-django/assets/62940515/9a36cee2-9c81-489c-95ab-a652fd869b4b)



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

![Screenshot 2024-06-12 113916](https://github.com/gerhash/wallet-django/assets/62940515/9f77a547-7e6e-4cca-a4c3-428671e4c9c9)


We now have a bread that contains transaction history.
They can be of 5 types, and they all contain quantity and date and time:

- Sent: Coin sent to user X 
- Received: Coin received from user X 
- Buy: Coin purchased
- Cashout: Coin Withdrawn
- Bonus: Coin Earned with bonusù

  ![Screenshot 2024-06-12 114022](https://github.com/gerhash/wallet-django/assets/62940515/09345e57-6b7f-41d5-a7b3-52fa0f8906f0)

Going down we have a dashboard that shows us the current value of the coin, with a graph (using Chart.js) that shows us its trend over time
  
  ![Screenshot 2024-06-12 114030](https://github.com/gerhash/wallet-django/assets/62940515/63d29284-eed5-4c76-a14c-87ac9aeaf0b4)


#### Account

![Screenshot 2024-06-12 114039](https://github.com/gerhash/wallet-django/assets/62940515/62f68c57-22d6-453f-928a-606fa527ff75)

In this section we have the avatar image at the top with username and other personal information
If the document verification has not been carried out, there is a button that reminds us to do it.

We have the wallet with the user's balance and then a screen that reminds us of the price of the coin, the invitation code and the ranking statistics and the number of people invited by us.
In the future it will be implemented by ensuring that rewards are obtained based on rank and people invited

## Database Logic

#### **Coin**

**id** | Coin primary Key id

**name** | Coin Name

**short** | Coin Shorter Name

**value** | Coin Value

#### **CustomUser**

**id** | User primary Key id

**username** | Username

**password** | Password
 
**email** | Email

**first_name** | First Name

**last_name** | Last Name

**cell** | Mobile Number

**balance** | User Balance (coin)

**code** | Share this code for receive Bonus

**invite_code** | The code you used for subscribe

**rank** | Your Ranking level, Gain badges and prizes

**score** | Invited Friends

**avatar_img** | Path to avatar_img

**dob** | Date of Birth

**city_b** | Birth City

**prov_b** | Birth Prov

**state_b** | Birth State

**addr_r** | Residence Address

**city_r** | Residence City

**prov_r** | Residence Prov

**state_r** | Residence State

**doc_n** | Doc Number

**doc_type** | Doc Type (CIE, Driver License, Passport)

**doc_location** | Where the document was created (municipality, DMV etc...)

**doc_city** | City where the document was created

**doc_state** | State where the document was created

**doc_bor** | Creation Date of document

**doc_exp** | Expiry Date of document

**doc_fr** | Path to Front Doc Image

**doc_rt** | Path to Retro Doc Image

**doc_selfie** | Path to Selfie  Image

**is_docverified** | Boolean too check verify

**last_login** | Last Login Date
  
**date_joined** | Account Creation Date

**is_superuser** | Full Permission 

**is_staff** | Staff Permission


#### **Calendar_record**

Track the prize change of the coin

**id** | Record primary Key id

**value** | Coin Value

**date** | Record Date

**coin_id** | Coind_id

#### **Transactions**

**id** | Transaction primary Key id

**type** | Type of transaction: BUY, SENT, RECEIVED, CASHOUT, BONUS

**tov** | Coin value at the transaction Moment (in FIAT)

**sender** | Sender username

**receiver** | Receiver username

**date** | Transaction Date

#### **Withdraw Req**

Request of Withdraw 

**id** | Request primary Key id

**quantity_req** | Amount of cashout

**iban** | Bank Details of the cashout 

**user** | User requested Withdraw

**date** | Request Date

#### **Bonus Codes**

**id** | Bonus primary Key id

**code** | Code String

**value** | Bonus Value

**creation_date** | Creation Date

**expiry_date** | Expiry Date

![Screenshot 2024-06-12 120431](https://github.com/gerhash/wallet-django/assets/62940515/154333e2-6379-4c34-a3c8-e5593fcdd22e)


