from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Transaction,Withdraw_requests
import random
import string
from .score_logic import *
import os
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, label="Email")
    username = forms.CharField(label="Username")
    avatar_img = forms.ImageField(required=False)
    invite_code = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Enter invite code'}))
    dob = forms.CharField(required=False)
    cell = forms.CharField(required=False)
    city_b = forms.CharField(required=False)
    prov_b = forms.CharField(required=False)
    state_b = forms.CharField(required=False)
    addr_r = forms.CharField(required=False)
    city_r = forms.CharField(required=False)
    prov_r = forms.CharField(required=False)
    state_r = forms.CharField(required=False)




    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2","invite_code","email", "cell", "avatar_img",
                  "first_name","last_name","dob", "city_b", "prov_b", "state_b", "addr_r", "city_r", "prov_r", "state_r"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Escludi i campi che iniziano con 'doc_' dal form
        for field_name in self.fields.keys():
            if field_name.startswith('doc_'):
                del self.fields[field_name]


    def save(self, commit=True):
        # Ottieni l'istanza dell'utente creato dal form
        user = super(RegisterForm, self).save(commit=False)



        # Genera un codice casuale di lunghezza TOT
        code_length = 10  # Lunghezza del codice desiderata
        unique_code_generated = False

        while not unique_code_generated:
            # Genera il codice casuale
            new_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=code_length))

            # Controlla se il codice generato è univoco
            if not CustomUser.objects.filter(code=new_code).exists():
                # Se il codice non esiste già nel database, lo impostiamo e usciamo dal ciclo
                user.code = new_code
                unique_code_generated = True
                # Rinomina il file dell'avatar
            if 'avatar_img' in self.cleaned_data:
                avatar_img = self.cleaned_data['avatar_img']
                if avatar_img:
                    # Rinomina il file dell'avatar
                    filename = f"avatar_{user.code}.{os.path.splitext(avatar_img.name)[1]}"
                    user.avatar_img.name = filename

        # Imposta balance e score a 0
        user.balance = 0
        user.rank = 0
        user.score = 0
        user.is_docverified = False
        if commit:
            user.save()
        return user




class DocumentUpdateForm(forms.ModelForm):
    doc_n = forms.CharField(required=False)
    doc_bor = forms.CharField(required=False)
    doc_exp = forms.CharField(required=False)
    doc_location = forms.CharField(required=False)
    doc_city = forms.CharField(required=False)
    doc_state = forms.CharField(required=False)
    doc_fr = forms.ImageField(required=False)
    doc_rt = forms.ImageField(required=False)
    doc_selfie = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['doc_type', 'doc_n', 'doc_bor', 'doc_exp', 'doc_location', 'doc_city', 'doc_state','doc_fr','doc_rt','doc_selfie']
#init
    def __init__(self, *args, **kwargs):
        super(DocumentUpdateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)

        print(self.cleaned_data)
        # Verifica se i file sono stati forniti
        if self.cleaned_data['doc_fr']:
            doc_fr = self.cleaned_data['doc_fr']
            user.doc_fr.name = f"front_{user.code}.{os.path.splitext(doc_fr.name)[1]}"

        if self.cleaned_data['doc_rt']:
            doc_rt = self.cleaned_data['doc_rt']
            user.doc_rt.name = f"retro_{user.code}.{os.path.splitext(doc_rt.name)[1]}"

        if self.cleaned_data['doc_selfie']:
            doc_selfie = self.cleaned_data['doc_selfie']
            user.doc_selfie.name = f"selfie_{user.code}.{os.path.splitext(doc_selfie.name)[1]}"


        #CAMBIA LOGICA IN MODO CHE L'UTENTE VADA CONFERMATO DAL PANNELLO ADMIN
        invite_score(user, DOCVERIFYB0NUS)
        user.is_docverified = True


        if commit:
            user.save()
        return user


TYPE_TRANSACTIONS = (
        ('IR', 'Invia o Ricevi'),
        ('BUY','Compra'),
        ('CASHOUT','Preleva')
    )
class SendCoinForm(forms.Form):
    value = forms.FloatField()
    receiver =  forms.CharField(max_length=150)
    class Meta:
        model = Transaction
        fields = ['value','receiver']

class BuyCoinForm(forms.Form):
    value = forms.FloatField()
    code = forms.CharField(max_length=12, required=False)  # per ora meglio di no

    class Meta:
        model = Transaction  # Maintain model association for potential future use
        fields = ['value','code']  # Include both fields in `fields`


class WithDrawForm(forms.Form):
    quantity_req = forms.FloatField()
    iban = forms.CharField(max_length=150)

    class Meta:
        model = Withdraw_requests
        fields = ['quantity_req','iban']