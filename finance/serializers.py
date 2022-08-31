from rest_framework import serializers

from .models import Currency, Category, Transaction


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = [
            'id',
            'code',
            'name'
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name'
        ]


class TransactionSerializer(serializers.ModelSerializer):
    # date = serializers.SerializerMethodField()
    #
    # def get_date(self, transaction: Transaction):
    #     return transaction.date.strftime("%Y-%m-%d %H:%M:%S")

    def to_representation(self, instance):
        representation = super(TransactionSerializer, self).to_representation(instance)
        representation['date'] = instance.date.strftime("%Y-%m-%d %H:%M:%S")
        return representation

    class Meta:
        model = Transaction
        fields = [
            'id',
            'amount',
            'currency',
            'descriptions',
            'category',
            'date',
        ]
