from rest_framework import serializers

from core.models import Account


class AccountSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=Account.TypeChoices,
        default=Account.TypeChoices.DEFAULT
    )

    class Meta:
        model = Account
        fields = "__all__"
