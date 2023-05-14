from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from core.models import Account
from core.serializers import AccountSerializer


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'number': openapi.Schema(type=openapi.TYPE_STRING, description='The Account Number.')
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
    if not account_number:
        response_message = {"error": "Account number is required"}
        response_status = HTTP_400_BAD_REQUEST
    else:
        account, created = Account.objects.get_or_create(balance=0, defaults={"number": account_number})
        if created:
            response_message = AccountSerializer(account).data
        else:
            response_message = {"error": "Account already exists."}
            response_status = HTTP_400_BAD_REQUEST

    return Response(response_message, status=response_status)
