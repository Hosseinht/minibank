from django.contrib import admin

from .models import Category,Currency,Transaction

admin.site.register(Category)
admin.site.register(Currency)
admin.site.register(Transaction)