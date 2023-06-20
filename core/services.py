import decimal
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK

from core.models import Account
from core.serializers import AccountSerializer

class BankAccountServices():
    def create_account_service(self, request):
        response_message: dict
        response_status = HTTP_201_CREATED

        account_number = request.data.get("number", None)
        account_type = request.data.get("type", Account.TypeChoices.DEFAULT)
        account_balance = request.data.get("balance", None)
        if not account_number or account_balance is None:
            response_message = {"error": "Account number and balance is required"}
            response_status = HTTP_400_BAD_REQUEST
        else:
            account = {
                'number': account_number,
                'type': account_type,
                'score': None,
                'balance': float(account_balance)
            }

            if account_type == Account.TypeChoices.BONUS:
                account['score'] = 10
            
            account, created = Account.objects.get_or_create(**account)
            if created:
                response_message = AccountSerializer(account).data
            else:
                response_message = {"error": "Account already exists."}
                response_status = HTTP_400_BAD_REQUEST
        
        return response_message, response_status

    def check_ballance_and_get_account_service(self, request):
        account_number = request.query_params.get('account_number')
        if not account_number:
            return {"error": "Account number is required in query parameters."}, HTTP_400_BAD_REQUEST
        try:
            account = Account.objects.get(number=account_number)
            serializer = AccountSerializer(account)
            return serializer.data, HTTP_200_OK
        except Account.DoesNotExist:
            return {"error": f"Account with number {account_number} not found."}, HTTP_404_NOT_FOUND
    
    def credit_account_service(self, request):
        account_number = request.data.get('number')
        amount = request.data.get('amount')

        if not account_number:
            return {"error": "Account number is required in request body."}, HTTP_400_BAD_REQUEST
        if not amount or amount <= 0:
            return {"error": "Amount must be greater than 0."}, HTTP_400_BAD_REQUEST

        try:
            account = Account.objects.get(number=account_number)
            account.balance += decimal.Decimal(amount)

            if account.type == Account.TypeChoices.BONUS:
                account.score += int(amount / 100)

            account.save()
            serializer = AccountSerializer(account)
            return serializer.data, HTTP_200_OK
        except Account.DoesNotExist:
            return {"error": f"Account with number {account_number} not found."}, HTTP_404_NOT_FOUND
    
    def debit_account_service(self, request):
        account_number = request.data.get('number')
        amount = request.data.get('amount')

        if not account_number:
            return {"error": "Account number is required in request body."}, HTTP_400_BAD_REQUEST
        if not amount or amount <= 0:
            return {"error": "Amount must be greater than 0."}, HTTP_400_BAD_REQUEST

        accounts_to_check = (Account.TypeChoices.DEFAULT, Account.TypeChoices.BONUS)
        try:
            account = Account.objects.get(number=account_number)
            account.balance -= decimal.Decimal(amount)

            if account.balance <= -1000 and account.type in accounts_to_check:
                return {"error": "The balance must be greater than -1000 for the Bonus and Default Accounts."}, HTTP_400_BAD_REQUEST

            account.save()
            serializer = AccountSerializer(account)
            return serializer.data, HTTP_200_OK
        except Account.DoesNotExist:
            return {"error": f"Account with number {account_number} not found."}, HTTP_404_NOT_FOUND