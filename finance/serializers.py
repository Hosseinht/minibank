from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Currency, Category, Transaction
from .reports import ReportParams

User = get_user_model()


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = fields


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = [
            'id',
            'code',
            'name'
        ]


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'user',
        ]


class TransactionReadSerializer(serializers.ModelSerializer):
    user = UserReadSerializer()
    currency = serializers.SlugRelatedField(slug_field='code', queryset=Currency.objects.all())
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    def to_representation(self, instance):
        representation = super(TransactionReadSerializer, self).to_representation(instance)
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
            'user'
        ]
        read_only_fields = fields


class TransactionWriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    currency = serializers.SlugRelatedField(slug_field='code', queryset=Currency.objects.all())
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    def to_representation(self, instance):
        representation = super(TransactionWriteSerializer, self).to_representation(instance)
        representation['date'] = instance.date.strftime("%Y-%m-%d %H:%M:%S")
        return representation

    class Meta:
        model = Transaction
        fields = [
            'user',
            'amount',
            'currency',
            'descriptions',
            'category',
            'date',
        ]

    def __init__(self, *args, **kwargs):
        # __init__ will be called just one time when you create an instance
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        # we need user from the context. we only have this information during request-response cycle. so here is where
        # we retrieve the user that made the request that is using this serializer
        self.fields['category'].queryset = Category.objects.filter(user=user)
        # self.fields['category'].queryset = user.categories.all()
        # so here we filtered category base on the user who created it. and other users can use this category to make
        # a transaction


class ReportEntrySerializer(serializers.Serializer):
    category = CategorySerializer()
    total = serializers.DecimalField(max_digits=15, decimal_places=2)
    count = serializers.IntegerField()
    avg = serializers.DecimalField(max_digits=15, decimal_places=2)


class ReportParamsSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        return ReportParams(**validated_data)
