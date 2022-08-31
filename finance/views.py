from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from .models import Currency, Category, Transaction
from .serializers import CurrencySerializer, CategorySerializer, TransactionSerializer


class CurrencyListView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
