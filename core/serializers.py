from rest_framework import serializers

from core.models import Account


class NestedDealProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
