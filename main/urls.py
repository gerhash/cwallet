from django.urls import path
from . import views
from . import crea_records

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('account', views.account, name='account'),
    path('verify-docs', views.verify_doc, name='verify_docs'),
    path('send', views.send_coin, name='send_coin'),
    path('receive', views.receive, name='receive'),
    path('buy', views.buy_coin, name='buy'),
    path('withdraw', views.withdraw, name='withdraw'),
    path('gen', views.gen, name='gen'),
]