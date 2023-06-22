import decimal

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK

from core.models import Account
from core.serializers import AccountSerializer
from core.services import BankAccountServices

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'number': openapi.Schema(type=openapi.TYPE_STRING, description='The Account Number.'),
            'type': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='The Account Type.',
                enum=['default', 'bonus', 'savings']
            ),
            'balance': openapi.Schema(type=openapi.TYPE_NUMBER, description='The Account Balance.'),
        }
    ),
    responses={
        HTTP_201_CREATED: openapi.Response('Account created', AccountSerializer),
        HTTP_400_BAD_REQUEST: openapi.Response("Error on creation")
    }
)
@api_view(["POST"])
def create_account(request):
    bank_account_service = BankAccountServices()

    response_message, response_status = bank_account_service.create_account_service(request)

    return Response(response_message, status=response_status)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('account_number', openapi.IN_QUERY, description="Account Number", type=openapi.TYPE_STRING)
    ],
    responses={
        200: openapi.Response('Success', AccountSerializer),
        400: "Bad Request",
        404: "Not Found"
    }
)
@api_view(["GET"])
def check_balance(request):
    bank_account_service = BankAccountServices()

    response_message, response_status = bank_account_service.check_ballance_and_get_account_service(request)

    return Response(response_message, status=response_status)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'number': openapi.Schema(type=openapi.TYPE_STRING, description='The Account Number.'),
            'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='The amount to credit to the account.')
        }
    ),
    responses={
        200: openapi.Response('Success', AccountSerializer),
        400: "Bad Request",
        404: "Not Found"
    }
)
@api_view(["POST"])
def credit_account(request):
    bank_account_service = BankAccountServices()

    response_message, response_status = bank_account_service.credit_account_service(request)

    return Response(response_message, status=response_status)
    

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'number': openapi.Schema(type=openapi.TYPE_STRING, description='The Account Number.'),
            'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='The amount to debit from the account.')
        }
    ),
    responses={
        200: openapi.Response('Success', AccountSerializer),
        400: "Bad Request",
        404: "Not Found"
    }
)
@api_view(["POST"])
def debit_account(request):
    account_number = request.data.get('number')
    amount = request.data.get('amount')

    if not account_number:
        return Response({"error": "Account number is required in request body."}, status=HTTP_400_BAD_REQUEST)
    if not amount or amount <= 0:
        return Response({"error": "Amount must be greater than 0."}, status=HTTP_400_BAD_REQUEST)

    accounts_to_check = (Account.TypeChoices.DEFAULT, Account.TypeChoices.BONUS)
    try:
        account = Account.objects.get(number=account_number)
        account.balance -= decimal.Decimal(amount)

        if account.balance <= -1000 and account.type in accounts_to_check:
            return Response(
                {"error": "The balance must be greater than -1000 for the Bonus and Default Accounts."},
                status=HTTP_400_BAD_REQUEST
            )

        account.save()
        serializer = AccountSerializer(account)
        return Response(serializer.data)
    except Account.DoesNotExist:
        return Response({"error": f"Account with number {account_number} not found."}, status=HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'origin_number': openapi.Schema(type=openapi.TYPE_STRING, description='The origin Account Number.'),
            'destination_number': openapi.Schema(type=openapi.TYPE_STRING, description='The destination Account Number.'),
            'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='The amount to debit from the account.')
        }
    ),
    responses={
        200: openapi.Response('Success', AccountSerializer(many=True)),
        400: "Bad Request",
        404: "Not Found"
    }
)
@api_view(["POST"])
def transfer_between_accounts(request):
    origin_account_number = request.data.get('origin_number')
    destination_account_number = request.data.get('destination_number')
    amount = request.data.get('amount')

    if not origin_account_number:
        return Response({"error": "Origin account number is required in request body."}, status=HTTP_400_BAD_REQUEST)
    if not destination_account_number:
        return Response({"error": "Destination account number is required in request body."}, status=HTTP_400_BAD_REQUEST)
    if not amount or amount <= 0:
        return Response({"error": "Amount must be greater than 0."}, status=HTTP_400_BAD_REQUEST)

    try:
        origin_account = Account.objects.get(number=origin_account_number)
        if origin_account.balance < amount:
            return Response({"error": "Amount must be lower than Account balance."}, status=HTTP_400_BAD_REQUEST)

        origin_account.balance -= decimal.Decimal(amount)
    except Account.DoesNotExist:
        return Response({"error": f"Account with number {origin_account_number} not found."}, status=HTTP_404_NOT_FOUND)

    try:
        destination_account = Account.objects.get(number=destination_account_number)
        destination_account.balance += decimal.Decimal(amount)

        if destination_account.type == Account.TypeChoices.BONUS:
            destination_account.score += int(amount / 150)
    except Account.DoesNotExist:
        return Response({"error": f"Account with number {destination_account_number} not found."}, status=HTTP_404_NOT_FOUND)

    origin_account.save()
    destination_account.save()
    serializer = AccountSerializer([origin_account, destination_account], many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'number': openapi.Schema(type=openapi.TYPE_STRING, description='The Account Number.'),
            'interest_percentage': openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description='Interest percentage to yield the amount.'
            )
        }
    ),
    responses={
        200: openapi.Response('Success', AccountSerializer),
        400: "Bad Request",
        404: "Not Found"
    }
)
@api_view(["POST"])
def yield_interest(request):
    response_message: dict
    response_status = HTTP_200_OK

    account_number = request.data.get('number')
    interest_percentage = request.data.get('interest_percentage')

    if not account_number:
        response_message = {"error": "Account number is required in request body."}
        response_status = HTTP_400_BAD_REQUEST
    elif not interest_percentage or interest_percentage <= 0:
        response_message = {"error": "Interest percentage must be greater than 0."}
        response_status = HTTP_400_BAD_REQUEST
    else:
        try:
            account = Account.objects.get(number=account_number)
            if account.type != Account.TypeChoices.SAVINGS:
                response_message = {"error": f"Account with number {account_number} is not a Savings Account."}
                response_status = HTTP_404_NOT_FOUND
            else:
                account.balance *= decimal.Decimal((interest_percentage / 100) + 1)
                account.save()
                serializer = AccountSerializer(account)
                response_message = serializer.data
        except Account.DoesNotExist:
            response_message = {"error": f"Account with number {account_number} not found."}
            response_status = HTTP_404_NOT_FOUND

    return Response(response_message, status=response_status)
