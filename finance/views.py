from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Currency, Category, Transaction
from .serializers import CurrencySerializer, CategorySerializer, TransactionWriteSerializer, TransactionReadSerializer


class CurrencyListView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = None


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    # pagination_class = None

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    # the result is filtered based on authenticated user. but user still can use categories that other users created.
    # to fix this issue we override init method in serializer


class TransactionViewSet(ModelViewSet):
    # queryset = Transaction.objects.select_related('category', 'currency', 'user')
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['description']
    ordering_fields = ["category", "currency", "date", "amount"]

    def get_queryset(self):
        return Transaction.objects.select_related('category', 'currency', 'user').filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TransactionReadSerializer
        return TransactionWriteSerializer

    # def perform_create(self, serializer):
    #     # in generic view there is method called create. create method call a method named performed_create which calls
    #     # save method. we can override it to add the authenticated user while creating a Transaction instance
    #     serializer.save(user=self.request.user)
    #     # the alternative way is to use HiddenField in serializer
