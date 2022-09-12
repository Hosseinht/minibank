```python
import random
from finance.models import Transaction, Currency, Category
from decimal import Decimal
from django.utils import timezone

txs = []

currencies = list(Currency.objects.all())
categories = list(Category.objects.all())

for i in range(1000):
    tx = Transaction(amount=random.randrange(Decimal(1), Decimal(1000)), currency=random.choice(currencies),
                     descriptions="", date=timezone.now() - timezone.timedelta(days=random.randint(1, 365)),
                     category=random.choice(categories))
    txs.append(tx)

Transaction.objects.bulk_create(txs)
```