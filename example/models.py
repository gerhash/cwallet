from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import datetime
class CustomUser(AbstractUser):
    #Dynamic Data
    cell = models.CharField(max_length=20)
    balance = models.FloatField(null=True, blank=True)
    code = models.CharField(max_length=16)
    invite_code = models.CharField(max_length=16,default='')
    score = models.IntegerField(null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    avatar_img = models.FileField(upload_to='avatar_img/')
    #Anagraphic Data
    dob = models.CharField(null=True, blank=True, max_length=10)
    city_b = models.CharField(max_length=50)
    prov_b = models.CharField(max_length=2)
    state_b = models.CharField(max_length=20)
    addr_r = models.CharField(max_length=200)
    city_r = models.CharField(max_length=200)
    prov_r = models.CharField(max_length=2)
    state_r = models.CharField(max_length=20)
    #ID DATA
    is_docverified = models.BooleanField(null=True)
    doc_type = models.CharField(max_length=50)
    doc_n = models.CharField(max_length=20)
    doc_bor = models.CharField(max_length=20)   #data emissione
    doc_exp = models.CharField(max_length=20)   #data scadenza
    doc_location = models.CharField(max_length=20)  #comune,questura
    doc_city = models.CharField(max_length=20)
    doc_state = models.CharField(max_length=20)
    doc_fr = models.FileField(upload_to='front_img/')
    doc_rt = models.FileField(upload_to='retro_img/')
    doc_selfie = models.FileField(upload_to='selfie_img/')




class Coin(models.Model):
    name = models.CharField(max_length=50)
    short = models.CharField(max_length=6)
    value = models.FloatField()

    def __str__(self):
        return self.name


class Calendar_record(models.Model):
    value = models.FloatField()
    date = models.DateTimeField()
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} - {self.coin.name} - {self.value}"

class Bonus_codes(models.Model):
    code = models.CharField(max_length=32, unique=True)  # Ensure unique codes
    value = models.FloatField()
    creation_date = models.DateTimeField(auto_now_add=True)  # Set on creation
    expiry_date = models.DateTimeField(blank=True, null=True)  # Optional expiry

    def is_valid(self):
        now = datetime.datetime.now()
        raw_issue = self.expiry_date
        current = now.strftime("%m/%d/%Y, %H:%M:%S")
        issue = raw_issue.strftime("%m/%d/%Y, %H:%M:%S")

        if issue > current:
            return True
        elif current > issue:
            return False
        else:
            return False


    class Meta:
        ordering = ['-creation_date']  # Order by creation date (newest first)

class Transaction(models.Model):

    type = models.CharField(max_length=30)
    value = models.FloatField()
    tov = models.FloatField()#valore in euro della transazione in quel momento
    sender = models.CharField(max_length=150)#chi invia
    receiver = models.CharField(max_length=150)  # chi riceve
    date = models.DateTimeField(default='Europe/Rome')


class Withdraw_requests(models.Model):
    quantity_req = models.FloatField()
    iban = models.CharField(max_length=150)
    user = models.CharField(max_length=150)
    date = models.DateTimeField(default='Europe/Rome')