import datetime
from dataclasses import dataclass
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import Sum, Count, Avg

from .models import Transaction, Category

User = get_user_model()


@dataclass
class ReportEntry:
    category: Category
    total: Decimal
    count: int
    avg: Decimal


@dataclass
class ReportParams:
    start_date: datetime.datetime
    end_date: datetime.datetime
    user: User


def transaction_report(params: ReportParams):
    data = []
    # filter authenticated user. each user sees his own report not others
    queryset = Transaction.objects.filter(
        user=params.user,
        date__gte=params.start_date,
        date__lte=params.end_date
    ).values('category').annotate(
        total=Sum('amount'),
        count=Count('id'),
        avg=Avg('amount')
    )

    # create index of category
    category_index = {}
    for category in Category.objects.filter(user=params.user):
        category_index[category.pk] = category

    for entry in queryset:
        category = category_index.get(entry["category"])
        report_entry = ReportEntry(
            category,
            entry['total'],
            entry['count'],
            entry['avg']
        )
        data.append(report_entry)
    return data

# without optimization
# def transaction_report():
#     data = []
#     queryset = Transaction.objects.values('category').annotate(
#         total=Sum('amount'),
#         count=Count('id'),
#         avg=Avg('amount')
#     )
#
#     for entry in queryset:
#         category = Category.objects.get(pk=entry["category"])
#         report_entry = ReportEntry(
#             category,
#             entry['total'],
#             entry['count'],
#             entry['avg']
#         )
#         data.append(report_entry)
#     return data
