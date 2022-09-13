from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CurrencyListView, CategoryViewSet, TransactionViewSet,TransactionReportAPIView

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
                  path("currencies/", CurrencyListView.as_view()),
                  path("report/", TransactionReportAPIView.as_view()),

              ] + router.urls
