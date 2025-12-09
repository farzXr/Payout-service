from rest_framework import serializers

from .models import Currency, Payout, PayoutStatus


class PayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "status")

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма должна быть положительной")
        return value

    def validate_recipient_details(self, value):
        if "account_holder" not in value:
            raise serializers.ValidationError("Отсутствует account_holder в реквизитах")
        return value

    def validate_currency(self, value):
        supported_currencies = dict(Currency.choices).keys()
        if value not in supported_currencies:
            raise serializers.ValidationError(
                f"Валюта {value} не поддерживается. Доступные: {', '.join(supported_currencies)}"
            )
        return value
