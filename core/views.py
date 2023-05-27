from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from core.models import Account
from core.serializers import AccountSerializer


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'number': openapi.Schema(type=openapi.TYPE_STRING, description='The Account Number.'),
            'balance': openapi.Schema(type=openapi.TYPE_NUMBER, description='The Account Balance.')
        }
    ),
    responses={
        HTTP_201_CREATED: openapi.Response('Account created', AccountSerializer),
        HTTP_400_BAD_REQUEST: openapi.Response("Error on creation")
    }
)
@api_view(["POST"])
def create_account(request):
    response_message: dict
    response_status = HTTP_201_CREATED

    account_number = request.data.get("number", None)
    account_balance = request.data.get("balance", None)
    if not account_number or account_balance is None:
        response_message = {"error": "Account number and balance is required"}
        response_status = HTTP_400_BAD_REQUEST
    else:
        account_balance = float(account_balance)
        account, created = Account.objects.get_or_create(balance=account_balance, defaults={"number": account_number})
        if created:
            response_message = AccountSerializer(account).data
        else:
            response_message = {"error": "Account already exists."}
            response_status = HTTP_400_BAD_REQUEST

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
    account_number = request.query_params.get('account_number')
    if not account_number:
        return Response({"error": "Account number is required in query parameters."}, status=HTTP_400_BAD_REQUEST)
    try:
        account = Account.objects.get(number=account_number)
        serializer = AccountSerializer(account)
        return Response(serializer.data)
    except Account.DoesNotExist:
        return Response({"error": f"Account with number {account_number} not found."}, status=HTTP_404_NOT_FOUND)


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
    account_number = request.data.get('number')
    amount = request.data.get('amount')

    if not account_number:
        return Response({"error": "Account number is required in request body."}, status=HTTP_400_BAD_REQUEST)
    if not amount or amount <= 0:
        return Response({"error": "Amount must be greater than 0."}, status=HTTP_400_BAD_REQUEST)

    try:
        account = Account.objects.get(number=account_number)
        account.balance += amount
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

    try:
        account = Account.objects.get(number=account_number)
        account.balance -= amount
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

        origin_account.balance -= amount
    except Account.DoesNotExist:
        return Response({"error": f"Account with number {origin_account_number} not found."}, status=HTTP_404_NOT_FOUND)

    try:
        destination_account = Account.objects.get(number=destination_account_number)
        destination_account.balance += amount
    except Account.DoesNotExist:
        return Response({"error": f"Account with number {destination_account_number} not found."}, status=HTTP_404_NOT_FOUND)

    origin_account.save()
    destination_account.save()
    serializer = AccountSerializer([origin_account, destination_account], many=True)
    return Response(serializer.data)
