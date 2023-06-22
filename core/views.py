from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

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
    bank_account_service = BankAccountServices()

    response_message, response_status = bank_account_service.debit_account_service(request)

    return Response(response_message, status=response_status)


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
    bank_account_service = BankAccountServices()

    response_message, response_status = bank_account_service.transfer_between_accounts(request)

    return Response(response_message, status=response_status)


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
    bank_account_service = BankAccountServices()

    response_message, response_status = bank_account_service.yield_interest_account(request)

    return Response(response_message, status=response_status)
