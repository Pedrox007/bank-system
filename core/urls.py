from django.urls import path

from core.views import (
    create_account,
    check_balance,
    credit_account,
    debit_account,
    transfer_between_accounts,
    yield_interest,
)

urlpatterns = [
    path('create-account/', create_account, name='create-account'),
    path('check-balance/', check_balance, name='check-balance'),
    path('credit/', credit_account, name='credit_account'),
    path('debit/', debit_account, name='debit_account'),
    path('transfer/', transfer_between_accounts, name='transfer_between_accounts'),
    path('yield-interest/', yield_interest, name='yield_interest_account')
]
