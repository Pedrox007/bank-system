from django.urls import path

from core.views import create_account, check_balance, credit_account

urlpatterns = [
    path('create-account/',
         create_account,
         name='create-account'),
    path('check-balance/',
        check_balance,
        name='check-balance'),
    path('credit/', 
        credit_account,
        name='credit_account'),
]
