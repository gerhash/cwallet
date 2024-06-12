from django.contrib import admin
from .models import Coin,CustomUser,Calendar_record,Transaction,Bonus_codes
# Register your models here.
admin.site.register(Coin)
admin.site.register(CustomUser)
admin.site.register(Transaction)
admin.site.register(Bonus_codes)


admin.site.register(Calendar_record)
